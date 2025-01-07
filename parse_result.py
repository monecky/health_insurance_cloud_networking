import numpy as np
from matplotlib import pyplot as plt
from ripe.atlas.cousteau import ProbeRequest, AtlasResultsRequest
from ripe.atlas.sagan import  TracerouteResult
import requests
import json
filters = {"tags": "system-anchor,system-ipv4-stable-90d,system-ipv6-stable-90d", "country_code": "NL",  "is_public":"True"}
probes = ProbeRequest(**filters)
list_probes = []
for probe in probes:
    list_probes += [probe["id"]]
list_ips = []
for i in range(104):
    kwargs = {
        "msm_id":85848140+i,
        "probe_ids": list_probes
    }

    is_success, results = AtlasResultsRequest(**kwargs).create()

    if is_success:
        for result in results:
            res = TracerouteResult(result)
            if(res.is_success):
                x = "success"
                print(res.ip_path)
                print(res.destination_name)
                print(res.destination_address)
                print(res.destination_ip_responded)
                list_ips.append(res.destination_address)
                # print("success")
            # else:
                # print("no_succes")
                # print(res.source_address)
                # print(res.destination_name)
            # res.
        print("hallo")
    else:
        print("Error loading request.")
        print(results)


def get_json_data(ip:str):
    # URL for the API request
    url = "https://stat.ripe.net/data/rir-stats-country/data.json?resource=" + ip

    # Send the GET request to the specified URL
    response = requests.get(url)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()

        # Optionally, print the JSON data (pretty-printed)
        # print(json.dumps(data, indent=4))

        return data
    else:
        print(f"Error: Unable to fetch data. HTTP Status code: {response.status_code}")
        return None
# print(get_json_data())
data = get_json_data("2001:67c:2e8::/48")
dns_register = [ get_json_data(ip)['data']['located_resources'][0]['location'] for ip in list_ips]
# print([ get_json_data(ip)['data']['located_resources'][0]['location'] for ip in list_ips])
# print(data['data']['located_resources'][0]['location'])
print(dns_register.count("US") + dns_register.count("NL"))
print(len(dns_register))
y = np.array([dns_register.count("US"), dns_register.count("NL")])
mylabels = ["US", "NL"]

plt.pie(y, labels = mylabels)
plt.show()
# https://stat.ripe.net/docs/02.data-api/rir-stats-country.html
# How to find the country https://stat.ripe.net/data/rir-stats-country/data.json?resource=2001:67c:2e8::/48
