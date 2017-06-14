import boto
import boto3
import constants
import json
import simpleS3Client

KeyToStartAfter = "raw/dump-1497431436"
client = boto3.client('s3', aws_access_key_id=constants.ACCESS_KEY, aws_secret_access_key=constants.SECRET_KEY)
paginator = client.get_paginator('list_objects_v2')
page_iterator = paginator.paginate(Bucket=constants.BUCKET_NAME, Prefix="raw/", StartAfter=KeyToStartAfter)
for page in page_iterator:
	if "Contents" in page:
		for key in page["Contents"]:
			keyString = key["Key"]
			coins = json.loads(simpleS3Client.readFromS3(keyString))
			print len(coins)
			content = ""
			for coin in coins:
				content += json.dumps(coin) + '\n'
			relativePathName = keyString.split("/")[1]
			filename = "processed/" + relativePathName
			print "Writing to key: " + filename
			simpleS3Client.writeToS3(filename, content)

