from base64 import standard_b64decode
from json import loads
from os import environ
from urllib.request import build_opener
import logging

secret_token = environ.get('AWS_SESSION_TOKEN')
secret_name = environ.get('Secret')

log = logging.getLogger()
log.setLevel(environ.get('Log_Level'))

def handler(event, context):
	log.info(event)
	response = {
		"isAuthorized": False,
		"context": {}
	}

	try:
		opener = build_opener()
		opener.addheaders = [("X-Aws-Parameters-Secrets-Token", secret_token)]
		with opener.open("http://localhost:2773/secretsmanager/get?secretId=" + secret_name) as r:
			secret = loads(loads(r.read().decode('utf-8'))["SecretString"])
			user_pass = standard_b64decode((event["headers"]["authorization"].split(" "))[1]).decode("utf-8").split(":")
			if (user_pass[0] == secret["username"] and user_pass[1] == secret["password"]):
				response["isAuthorized"] = True
				log.info('allowed')
			else:
				log.info('denied')
				
		return response
		
	except BaseException as e:
		log.error(e)
		return response
