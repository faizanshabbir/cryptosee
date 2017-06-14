import boto
import boto3
import constants
import json

i=0
client = boto3.client('s3', aws_access_key_id=constants.ACCESS_KEY, aws_secret_access_key=constants.SECRET_KEY)
paginator = client.get_paginator('list_objects_v2')
page_iterator = paginator.paginate(Bucket=constants.BUCKET_NAME, Prefix="raw/", StartAfter="raw/dump-1495875601")
for page in page_iterator:
	if "Contents" in page:
		for key in page["Contents"]:
			keyString = key["Key"]
			print keyString
			objresp = client.get_object(Bucket=constants.BUCKET_NAME, Key=keyString)
			body = objresp['Body'].read()
			coins = json.loads(body)
			content = ""
			for coin in coins:
				content += json.dumps(coin) + '\n'
			relativePathName = keyString.split("/")[1]
			filename = "processed/" + relativePathName
			i += 1
			print "Writing to key: " + filename
			print i
			s3_conn = boto.connect_s3(constants.ACCESS_KEY, constants.SECRET_KEY)
			bucket = s3_conn.get_bucket(constants.BUCKET_NAME)
			keyToWrite = boto.s3.key.Key(bucket, filename)
			keyToWrite.set_contents_from_string(content)

