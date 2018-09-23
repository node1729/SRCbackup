import json
import certifi
import urllib3

http = urllib3.PoolManager(
        cert_reqs="CERT_REQUIRED",
        ca_certs=certifi.where())

game = "pikmin2"
category = "Pay_Off_Debt"

r = http.request("GET", "http://speedrun.com/api/v1/leaderboards/" + game + "/category/" + category,
        headers={
            "User-Agent": "backupbot v0.01 by node1729 (on GitHub)"
            })

outJSON = open("output.json", "w")

test = json.loads(r.data.decode("utf-8"))

json.dump(test, outJSON, indent=4)
