#!/usr/bin/env python3

import requests
import json
import boto3

access_key = "XXXXXX"
secret_access_key = "XXXX" 
hosted_zone_id = "XXXXX"
public_domain = "XXXX"

### This is the API call that checks your current IP address ###
response = requests.get("https://api.ipify.org?format=json")
while response.status_code != 200:
    reponse = requests.get("https://api.ipify.org?format=json")

public_ip = response.json()["ip"]

client = boto3.client(
    "route53",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_access_key
)

record_set = client.list_resource_record_sets(HostedZoneId=hosted_zone_id)

# print(json.dumps(record_set, indent=2))

for record in record_set["ResourceRecordSets"]:
    if record["Name"] == public_domain:
        if public_ip == record["ResourceRecords"][0]["Value"]:
            print("SAME PUBLIC IP FOR DOMAIN "+public_domain)
            break
        else:
            response = client.change_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                ChangeBatch={
                    "Comment": "Change the record for the new public ip address",
                    "Changes": [
                        {
                            "Action": "UPSERT",
                            "ResourceRecordSet": {
                                "Name": public_domain,
                                "Type": "A",
                                "TTL": 60,
                                "ResourceRecords": [
                                    {
                                    "Value": public_ip
                                    }
                                ]
                            }
                        }
                    ]
                }
            )
            print("YOUR PUBLIC IP CHANGED TO "+public_ip+" for domain "+public_domain)
            break








