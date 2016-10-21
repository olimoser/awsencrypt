from __future__ import print_function
import boto3
import json

session = boto3.Session(profile_name="codecentric")
s3 = session.client("s3")
kms = session.client("kms")

print(json.dumps(kms.list_keys(), indent=2))