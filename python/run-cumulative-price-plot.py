import time
import datetime
import boto3
import json
import matplotlib
import matplotlib.dates
import matplotlib.pyplot
import constants
from optparse import OptionParser

def convertDateToTime(fromDate):
	dateObj = datetime.datetime.strptime(fromDate, "%Y-%m-%d %H:%M:%S")
	return time.mktime(dateObj.timetuple())

def getPartialTime(fromDate):
	fromDate = fromDate[:-9]
	dateObj = datetime.datetime.strptime(fromDate, "%Y-%m-%d")
	return time.mktime(dateObj.timetuple())

def main():
	startDate = "2017-05-25 10:00:00"
	endDate = "2017-05-28 10:00:00"

	startTime = convertDateToTime(startDate)
	endTime = convertDateToTime(endDate)

	begTime = int(getPartialTime(startDate))
	print begTime
	finTime = int(getPartialTime(endDate))
	print finTime

	symbol = "Ethereum"

	time1 = time.time()
	objectListv2 = []
	commonPrefix = "dump-"
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
	print time.time() - time1

	times = []
	prices = []
	for i, keyString in enumerate(objectListv2):
		objResp = client.get_object(Bucket=constants.BUCKET_NAME, Key=keyString)
		body = objResp['Body'].read()
		jsonBody = json.loads(body)
		coin = [obj for obj in jsonBody if(obj['name'] == symbol)]
		prices.append(coin[0]['price_usd'])
		times.append(datetime.datetime.fromtimestamp(float(coin[0]['last_updated'])))
		print str(i) + "th file processed"

	dates = matplotlib.dates.date2num(times)

	matplotlib.pyplot.plot_date(dates, prices)
	matplotlib.pyplot.show()

if __name__ == "__main__":
    main()
