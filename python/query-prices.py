import urllib2
import json
import time
import requests
import boto
import boto.s3
from boto.s3.key import Key
import constants

response = requests.get("https://api.coinmarketcap.com/v1/ticker/")
coins = json.loads(response.content)

s3_conn = boto.connect_s3(constants.ACCESS_KEY, constants.SECRET_KEY)
bucket = s3_conn.get_bucket(constants.BUCKET_NAME)
currTime = str(time.time()).split(".")[0]
filename = "dump-" + currTime
print filename
key = boto.s3.key.Key(bucket, filename)

content = ""
for coin in coins:
	content += json.dumps(coin) + '\n'
print content
print "attempt to write key"
key.set_contents_from_string(content)



