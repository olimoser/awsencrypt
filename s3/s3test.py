from __future__ import print_function
import boto3

session = boto3.Session(profile_name="codecentric")
s3 = session.client("s3")
kms = session.client("kms")

print(kms.list_keys())