import socket

import pandas as pd
from ripe.atlas.cousteau import Traceroute, AtlasCreateRequest, AtlasSource, ProbeRequest, AtlasLatestRequest
from sqlalchemy import Result

file_path = "data_health_insurance.xlsx"
df = pd.read_excel(file_path, sheet_name=0)
print(df.columns)
companies = {}
for z in df.iterrows():
    i = z[1]
    companies[i['Company']] = [(i["Home Domain"],i["Home IPv6.1"], "Home")]
    if i["Registration vs Home"] == 0:
        companies[i['Company']] += [(i["Registration domain"],i["Registration IPv6.1"],"Registration")]
    else:
        companies[i['Company']] = [(i["Home Domain"],i["Home IPv6.1"], "Home;Registration")]
    if i["Login vs Home"] == 0:
        companies[i['Company']] += [(i["Login domain"],i["Login IPv6"],"Login")]
traceroutes = []
count = 0
for company in companies:
    for link in companies[company]:
        target = link[0]
        try:
            socket.gethostbyname(target)  # Check if the target is resolvable
        except socket.gaierror:
            print(f"Unresolvable target: {target}")
        traceroutes.append(
            Traceroute(
                af = 4,
                target = target,
                description="4"+target + ";" + link[2] + ";" + company,
                protocol = "UDP",
                resolve_on_probe = True,
                skip_dns_check = False,
            )
        )
        count += 1
        if link[1] == 1:
            traceroutes.append(
                Traceroute(
                     af = 6,
                     target = target,
                     description="4"+target+";"+link[2]+";"+company,
                     protocol="UDP",
                     resolve_on_probe=True,
                     skip_dns_check=False,
                )
            )
            count += 1
print(count)
print(300000 /(count*60))

filters = {"tags": "system-anchor,system-ipv4-stable-90d,system-ipv6-stable-90d", "country_code": "NL",  "is_public":"True"}
probes = ProbeRequest(**filters)
list_probes = []
for probe in probes:
    list_probes += [str(probe["id"])]
list_probes =  ",".join(list_probes)
print(probes.total_count)
# print(list_probes)
# If system-anchor is selected we remain with probes that handle IPv4 and IPv6
# when doing this for the Netherlands, 44 remain.
source = AtlasSource(
    type="probes",
    value=list_probes,
    requested=34,
    tags={"exclude":["broken"]}
)

# RIPE Atlas API Key (replace with your actual key)
RIPE_API_KEY = "696c7a0b-ae0f-409c-a199-b6327b49d4df"

# # Submit measurements
atlas_request = AtlasCreateRequest(
    key=RIPE_API_KEY,
    msm_id=202503012001,
    measurements=traceroutes,
    sources=[source],
    is_oneoff=True,
    start_time=None,  # Start immediately
    stop_time=None,   # Run indefinitely until finished
)
(is_success, response) = atlas_request.create()

if is_success:
    print(response)
else:
    print("Error making request")
    print(response)

