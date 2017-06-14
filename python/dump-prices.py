import urllib2
import json
import time
import requests
import boto
import boto.s3
from boto.s3.key import Key
import constants

def doCryptoCompareQuery(fromSymbols, toSymbols):
	priceBaseUrl = "https://min-api.cryptocompare.com/data/pricemulti"
	parameters = {"fsyms": fromSymbols, "tsyms": toSymbols}
	response = requests.get(priceBaseUrl, params = parameters)
	print type(response.status_code)
	if response.status_code is int(200):
		print "success"
		print response.content
		return response.content
	else:
		print "UNSUCCESSFUL"
		return -1
	# print response.content

response = requests.get("https://api.coinmarketcap.com/v1/ticker/")
coins = json.loads(response.content)

s3_conn = boto.connect_s3(constants.ACCESS_KEY, constants.SECRET_KEY)
bucket = s3_conn.get_bucket(constants.BUCKET_NAME)
currTime = str(time.time())
currTime = currTime[:-3]
filename = "test/dump-test3"
key = boto.s3.key.Key(bucket, filename)

content = ""
for coin in coins:
	content += json.dumps(coin) + '\n'
print content
print "attempt to write key"
key.set_contents_from_string(content)



