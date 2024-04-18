# Dyn53
Dyn53 is a serverless application for dynamic DNS.

## What
API Gateway exposes two identical api calls (`POST` and `PUT` to `/ddns`) under the `ddns.` sub domain name. This will permit updating any record in the specified hosted zone.

```mermaid
flowchart LR
	subgraph API_Gateway[API Gateway]
		direction TB
		subgraph /ddns
			direction RL
			POST
			PUT
		end
	end

	subgraph Lambda
		direction TB
		Authorizer
		Record_Setter[Record Setter]
	end

	subgraph Route53
		subgraph HostedZone
			ddns.example.com
			dyn.example.com
		end
	end

	subgraph Certificate Manager
		ddns.example.com_Certificate[ddns.example.com]
	end

	subgraph Secret Manager
		Secret
	end

	ddns.example.com_Certificate --> ddns.example.com --> API_Gateway
	API_Gateway --> Authorizer --> Secret
	POST --> Record_Setter
	PUT --> Record_Setter
	Record_Setter ---> dyn.example.com
```

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
* Parameterizing API domain name ([#1](https://github.com/AV-IO/Dyn53/issues/1))
* Option to opt-out of secret manager ([#2](https://github.com/AV-IO/Dyn53/issues/2))
  * While proper, it is by far the most expensive part of this deployment, and should be up to the user's choice
* Restrict Permissions to a set of sub domain names instead of to an entire hosted zone ([#3](https://github.com/AV-IO/Dyn53/issues/3))
