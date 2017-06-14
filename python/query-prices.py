import json
import time
import requests
import simpleS3Client

def main():
	response = requests.get("https://api.coinmarketcap.com/v1/ticker/")
	coins = json.loads(response.content)

	currTime = str(time.time()).split(".")[0]
	filename = "raw/dump-" + currTime

	print "Found information on " + str(len(coins)) + " coins for time: " + currTime 
	simpleS3Client.writeToS3(filename, json.dumps(coins))

if __name__ == "__main__":
    main()

