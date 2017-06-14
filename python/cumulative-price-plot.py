import time
import datetime
import boto3
import json
import matplotlib
import matplotlib.dates
import matplotlib.pyplot
import constants
import simpleS3Client

def convertDateToTime(fromDate):
	dateObj = datetime.datetime.strptime(fromDate, "%Y-%m-%d %H:%M:%S")
	return time.mktime(dateObj.timetuple())

def getPartialTime(fromDate):
	fromDate = fromDate[:-9]
	dateObj = datetime.datetime.strptime(fromDate, "%Y-%m-%d")
	return time.mktime(dateObj.timetuple())

def main():
	startDate = "2017-05-25 10:00:00"
	endDate = "2017-05-26 05:00:00"

	startTime = convertDateToTime(startDate)
	endTime = convertDateToTime(endDate)

	begTime = int(getPartialTime(startDate))
	print begTime
	finTime = int(getPartialTime(endDate))
	print finTime

	symbol = "Ethereum"

	objectListv2 = []
	commonPrefix = "raw/dump-"
	client = boto3.client('s3', aws_access_key_id=constants.ACCESS_KEY, aws_secret_access_key=constants.SECRET_KEY)
	paginator = client.get_paginator('list_objects_v2')
	for result in paginator.paginate(Bucket=constants.BUCKET_NAME, StartAfter=commonPrefix+str(begTime)):
		if "Contents" in result:
			for key in result["Contents"]:
				keyString = key["Key"]
				currTime = keyString.split("-")
				currTime = int(currTime[1])
				# S3 keys are returned in lexicographic order, so we can break if we exceed finTime
				if (currTime > finTime):
					break
				else:
					objectListv2.append(keyString)

	print str(len(objectListv2)) + " objects found to read"

	times = []
	prices = []
	for i, keyString in enumerate(objectListv2):
		jsonBody = json.loads(simpleS3Client.readFromS3(keyString))
		coin = [obj for obj in jsonBody if(obj['name'] == symbol)]
		prices.append(coin[0]['price_usd'])
		times.append(datetime.datetime.fromtimestamp(float(coin[0]['last_updated'])))
		print str(i) + "th file processed"

	dates = matplotlib.dates.date2num(times)

	matplotlib.pyplot.plot_date(dates, prices)
	matplotlib.pyplot.show()

if __name__ == "__main__":
    main()
