from ripe.atlas.cousteau import AtlasLatestRequest, ProbeRequest
from sqlalchemy import Result
filters = {"tags": "system-anchor,system-ipv4-stable-90d,system-ipv6-stable-90d", "country_code": "NL",  "is_public":"True"}
probes = ProbeRequest(**filters)
list_probes = []
for probe in probes:
    # print(probe["id"])
    # print(probe)
    list_probes += [probe["id"]]
kwargs = {
    "probe_ids": list_probes
}

is_success, results = AtlasLatestRequest(**kwargs).create()

if is_success:
    for result in results:
        print(Result.get(result))
else:
    print("Error loading request.")