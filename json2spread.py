import json
import csv
import urllib3

spreadsheet = open("output.csv", "w")

data = open("output.json")

data = json.load(data)

data = data["data"]

print(data["game"])



def httpReq(URL):

    http = urllib3.PoolManager()

    r = http.request("GET", URL,
            data=None,
            headers={
                "User-Agent": "backupbot v0.01 by node1729 (on GitHub)"
                })
    data = json.loads(r.data.decode("utf-8"))
        

with spreadsheet:
    fieldnames = ["place", "id", "weblink", "game", "level", "category", "videos", "comment", "status", "examiner", "verify-date", "players", "date", "submitted", "times", "system", "splits", "values"]

    writer = csv.DictWriter(spreadsheet, fieldnames=fieldnames)
    
    writer.writeheader()
    x = 0
    while x < len(data["runs"]):
        outDict = {"place": data["runs"][x]["place"]}
        for key in data["runs"][x]["run"]:
            outDict[key] = data["runs"][x]["run"][key]
        
#        for outKey in outDict:
#            if outKey == "game":
                 
        writer.writerow(outDict)
        x += 1


