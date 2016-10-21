# awsencrypt

some proof of concept scripts for AWS client side encryption with python boto3

## generate_key_material.py

generate an external AWS customer master key (CMK) with python boto3
can be used to derive data encryption keys for client side encryption

* creates an external master key if not exist
* gets import parameters from AWS API
* imports key material
* stores key material locally in key_material/*