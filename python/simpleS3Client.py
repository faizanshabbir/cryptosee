import boto
import boto.s3
from boto.s3.key import Key
import constants

def writeToS3(keyname, content):
	s3_conn = boto.connect_s3(constants.ACCESS_KEY, constants.SECRET_KEY)
	bucket = s3_conn.get_bucket(constants.BUCKET_NAME)
	key = boto.s3.key.Key(bucket, keyname)
	try:
		key.set_contents_from_string(content)
		print "Successfully wrote s3://" + constants.BUCKET_NAME + "/" + keyname
	except:
		print "Encountered error while attempting to write s3://" + constants.BUCKET_NAME + "/" + keyname

def readFromS3(keyname):
	s3_conn = boto.connect_s3(constants.ACCESS_KEY, constants.SECRET_KEY)
	bucket = s3_conn.get_bucket(constants.BUCKET_NAME)
	key = boto.s3.key.Key(bucket, keyname)
	try:
		content = key.get_contents_as_string()
		print "Successfully read s3://" + constants.BUCKET_NAME + "/" + keyname
		return content
	except:
		print "Encountered error while attempting to read s3://" + constants.BUCKET_NAME + "/" + keyname
		return False
