import json
import csv
import urllib3
import certifi
import re
import datetime

spreadsheet = open("output.csv", "w")

data = open("output.json")

data = json.load(data)

data = data["data"]

print(data["game"])



def httpReq(URL):

    http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where())

    r = http.request("GET", URL,
            headers={
                "User-Agent": "backupbot v0.01 by node1729 (on GitHub)"
                })

    output = json.loads(r.data.decode("utf-8"))

    output = output["data"]

    return output

with spreadsheet:
    fieldnames = ["place", "id", "weblink", "game", "level", "category", "videos", "comment", "status", "examiner", "verify-date", "players", "date", "submitted", "times", "system", "splits", "values"]

    writer = csv.DictWriter(spreadsheet, fieldnames=fieldnames)

    writer.writeheader()
    x = 0

    #Get Game and Category names.
    game = httpReq("https://speedrun.com/api/v1/games/" + data["game"])
    game = game["names"]["international"]
    category = httpReq("https://speedrun.com/api/v1/categories/" + data["category"])
    category = category["name"]

    playersDict = {}
    while x < len(data["runs"]):
        #build a new dictionary in order to write to the spreadsheet more effectively with place.
        outDict = {"place": data["runs"][x]["place"]}
        for key in data["runs"][x]["run"]:
            outDict[key] = data["runs"][x]["run"][key]
        try:
            videosLen = len(outDict["videos"]["links"])
        except TypeError:
            videosLen = 0
        for outKey in outDict:
            players = []
            playersStr = ""
            videos = []
            videosStr = ""
            splits = []
            splitsStr = ""
            #replaces id with human readable name
            if outKey == "game":
                outDict["game"] = game
            elif outKey == "category":
                outDict["category"] = category

            #get players
            elif outKey == "players":
                for item in outDict["players"]:
                    if item["rel"] == "guest":
                        players.append(re.split("]", item["name"])[1])
                    #convert user ID to real name
                    elif item["rel"] == "user":
                        if item["id"] not in playersDict:
                            user = httpReq("https://speedrun.com/api/v1/users/" + item["id"])
                            players.append(user["names"]["international"])
                            playersDict[item["id"]] = user["names"]["international"]
                            print("added to playersDict " + user["names"]["international"])
                        else:
                            user = playersDict[item["id"]]
                            players.append(user)

                    for item in players:
                        if item == players[-1]:
                            playersStr += item
                        else:
                            playersStr += item + "\r\n"
                outDict["players"] = playersStr

            #get videos
            elif outKey == "videos" and videosLen != 0:
                for key in outDict["videos"]:
                    for item in outDict["videos"][key]:
                        videos.append(item["uri"])
                for item in videos:
                    if item == videos[-1]:
                        videosStr += item
                    else:
                        videosStr += item + "\r\n"
                outDict["videos"] = videosStr

            #get platform and region
            elif outKey == "system":
                for key in outDict["system"]:
                    if key == "platform":
                        platform = httpReq("https://speedrun.com/api/v1/platforms/" + outDict["system"]["platform"])
                        platform = platform["name"]
                    elif key == "region":
                        region = httpReq("https://speedrun.com/api/v1/regions/" + outDict["system"]["region"])
                        region = region["name"]
                    elif key == "emulated":
                        if outDict["system"]["emulated"]:
                            emulated = " [EMU]"
                        else:
                            emulated = ""
                outDict["system"] = region + " " + platform + emulated

            #get verifier
            elif outKey == "status":
                for key in outDict["status"]:
                    if key == "examiner":
                        if outDict["status"]["examiner"] != None:
                            if outDict["status"]["examiner"] in playersDict:
                                examiner = playersDict[outDict["status"]["examiner"]]
                            else:
                                examiner = httpReq("https://speedrun.com/api/v1/users/" + outDict["status"]["examiner"])
                                examiner = examiner["names"]["international"]
                                playersDict[outDict["status"]["examiner"]] = examiner
                                print("added to playersDict " + examiner)
                        else:
                            examiner = "[UNKNOWN]"
                    elif key == "verify-date":
                        if outDict["status"]["verify-date"] != None:
                            dateVerified = outDict["status"]["verify-date"]
                        else:
                            dateVerified = "[UNKNOWN]"
                outDict["status"] = "Verified by " + examiner + " on " + dateVerified

            #get splits
            elif outKey == "splits" and outDict["splits"] != None:
                for key in outDict["splits"]:
                    if key == "uri":
                        outDict["splits"]["uri"] = outDict["splits"]["uri"].replace("api/v3/runs/", "")
                        outDict["splits"] = outDict["splits"]["uri"]
                        
            elif outKey == "times":
                for key in outDict["times"]:
                    if key == "primary_t":
                        second = int(outDict["times"]["primary_t"])
                        second = str(datetime.timedelta(seconds=second))
                outDict["times"] = second

        writer.writerow(outDict)
        x += 1
