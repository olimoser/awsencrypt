from __future__ import print_function
from datetime import datetime
import boto3
import json
import crypto


def serializer(s):
    if isinstance(s, datetime):
        return s.isoformat()


session = boto3.Session(profile_name="codecentric")
s3 = session.client("s3")
kms = session.client("kms")
FILE = "./plaintext.txt"


def list_my_keys():
    for key in kms.list_keys()['Keys']:
        print(json.dumps(kms.describe_key(KeyId=key['KeyId']),
                         default=serializer,
                         indent=2))

list_my_keys()

aws_master_key = "52e254a1-9438-4429-acda-4f2f1d933dd6"

data_key_request = kms.generate_data_key(KeyId=aws_master_key, KeySpec='AES_256')
print(data_key_request)


        #
        # key_request = kms.generate_data_key(KeyId=customer_key, KeySpec='AES_256')
        # key_plaintext = key_request['Plaintext']
        # key_cipher = key_request['CiphertextBlob']
        #
        # print(key_plaintext,key_request,key_cipher)
