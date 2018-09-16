import json

import urllib3

http = urllib3.PoolManager()

game = 
category = 

r = http.request("GET", "http://speedrun.com/api/v1/leaderboards/" + game + "/category/" + category,
        data=None,
        headers={
            "User-Agent": "backupbot v0.01 by node1729 (on GitHub)"
            })

outJSON = open("output.json", "w")

test = json.loads(r.data.decode("utf-8"))

json.dump(test, outJSON, indent=4)
