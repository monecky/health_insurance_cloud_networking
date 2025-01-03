from ripe.atlas.cousteau import ProbeRequest, AtlasResultsRequest
from ripe.atlas.sagan import Result, TracerouteResult
filters = {"tags": "system-anchor,system-ipv4-stable-90d,system-ipv6-stable-90d", "country_code": "NL",  "is_public":"True"}
probes = ProbeRequest(**filters)
list_probes = []
for probe in probes:
    list_probes += [probe["id"]]
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
                print("success")
            else:
                print("no_succes")
            # res.
        print("hallo")
    else:
        print("Error loading request.")
        print(results)