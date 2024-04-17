from boto3 import client
from botocore.exceptions import ClientError
from os import environ
from time import time
import logging

region = environ.get("AWS_REGION")
hosted_zone_id = environ.get("HostedZoneId")

log = logging.getLogger()
log.setLevel(environ.get('Log_Level'))

r53client = client('route53', region_name=region)

def handler(event, context):
	log.info(event)
	try:
		r53client.change_resource_record_sets(
			HostedZoneId=hosted_zone_id,
			ChangeBatch={
				"Comment": f"updated via dDNS Lambda setter at {time()}",
				"Changes": [
					{
						"Action": "UPSERT",
						"ResourceRecordSet": {
							"Name": event["queryStringParameters"]["hostname"],
							"Type": "A",
							"ResourceRecords": [
								{
									"Value": event["queryStringParameters"]["ip"]
								}
							],
							"TTL": 300
						}
					}
				]
			}
		)
	except ClientError as e:
		log.error(e)
		return {
			"statusCode": 500
		}
	log.info("success")
	return {
		"statusCode": 200
	}
