import boto3
import logging
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

session = boto3.Session(profile_name="codecentric")
s3 = session.client("s3")
kms = session.client("kms")


def serializer(s):
    if isinstance(s, datetime):
        return s.isoformat()

