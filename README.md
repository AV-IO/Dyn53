# Dyn53
Dyn53 is a serverless application for dynamic DNS.

## What
API Gateway exposes two identical api calls (`POST` and `PUT` to `/ddns`) under the `ddns.` sub domain name. This will permit updating any record in the specified hosted zone.

## Deploy
This application is fully SAM compatible and can be deployed with the following:
```sh
sam deploy --config-file ./samconfig.toml --config-env prod --region {region} --profile {profile} --parameter-overrides 'HostedZoneId=Z1234' 'DomainName=example.com' 'DynamicSubDomain=dyn'
```

## Why
Unifi Dynamic DNS options don't natively support Route53 (understandably), and there seems to be some terrible solutions out there so I made my own.

## How
Basic sequence is as follows:
```mermaid
sequenceDiagram
    participant User
    participant API Gateway
	participant Authorizer Lambda
	participant Setting Lambda
	participant Route53

    User ->>+ API Gateway: POST /ddns?hostname=dyn.example.com&ip=1.2.3.4
	API Gateway ->>+ Authorizer Lambda: Authorization: Basic dXNlcjpwYXNzd29yZA==
	Authorizer Lambda -->>- API Gateway: true
	API Gateway ->>+ Setting Lambda: {request data}
	Setting Lambda ->>+ Route53: UPSERT dyn.example.com A: 1.2.3.4
	Route53 -->>- Setting Lambda: 200
	Setting Lambda -->>- API Gateway: 200
    API Gateway-->>-User: HTTP 200
```

## Contributing
It's GNU GPLv3, feel free to send pull requests or file issues.

### Planned contributions
* parameterizing API domain name
  * lambda check to make sure you're not overwriting the api domain name