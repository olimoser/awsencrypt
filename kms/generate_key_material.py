import boto3
import logging
import base64
from subprocess import call

"""
generate an external AWS customer master key (CMK) with python boto3
can be used to derive data encryption keys for client side encryption

* creates an external master key if not exist
* gets import parameters from AWS API
* imports key material
* stores key material locally in key_material/*

"""

__author__ = "Oliver Moser"
__copyright__ = "Copyright 2016"
__license__ = "GPL"
__version__ = "0.0.1"

MASTER_KEY_NAME = "External_Master_Key"
ALIAS_PATTERN = "alias/{0}"
PLAINTEXT_KEY = "../key_material/PlaintextKeyMaterial.bin"
ENCRYPTED_KEY = "../key_material/EncryptedKeyMaterial.bin"
PUBLIC_KEY = "../key_material/public.key.bin"
PUBLIC_KEY_64 = PUBLIC_KEY + ".b64"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

session = boto3.Session(profile_name="codecentric")
kms = session.client("kms")


def generate_external_master_key(client):
    generated_key = client.create_key(
        Description=MASTER_KEY_NAME,
        KeyUsage='ENCRYPT_DECRYPT',
        Origin='EXTERNAL',
        BypassPolicyLockoutSafetyCheck=False
    )
    key_id = generated_key["KeyMetadata"]["KeyId"]
    logger.info("created master key {0}".format(key_id))

    key_alias = client.create_alias(
        AliasName=ALIAS_PATTERN.format(MASTER_KEY_NAME),
        TargetKeyId=key_id
    )
    logger.info("set alias {0}".format(key_alias))

    return key_id


def get_master_key(client, key_alias):
    aliases = client.list_aliases()
    for alias in aliases['Aliases']:
        if alias['AliasName'] == ALIAS_PATTERN.format(key_alias):
            return alias['TargetKeyId']
    return False


def import_key_material(client, key_id):
    import_parameters = client.get_parameters_for_import(
        KeyId=key_id,
        WrappingAlgorithm='RSAES_OAEP_SHA_1',
        WrappingKeySpec='RSA_2048'
    )
    import_token = import_parameters['ImportToken']
    public_key = import_parameters['PublicKey']
    public_key_b64 = base64.b64encode(import_parameters['PublicKey'])

    f = open(PUBLIC_KEY_64, 'w')
    f.write(public_key_b64)
    f.close()

    call(["openssl", "enc", "-d", "-base64", "-A", "-in", PUBLIC_KEY_64, "-out", PUBLIC_KEY])
    call(["openssl", "rand", "-out", PLAINTEXT_KEY, "32"])
    call(["openssl", "rsautl", "-encrypt", "-in", PLAINTEXT_KEY,
          "-oaep", "-inkey", PUBLIC_KEY, "-keyform", "DER",
          "-pubin", "-out", ENCRYPTED_KEY])

    f = open(ENCRYPTED_KEY, "rb")
    key_material = f.read()
    f.close()

    client.import_key_material(
        KeyId=key_id,
        ImportToken=import_token,
        EncryptedKeyMaterial=key_material,
        ExpirationModel='KEY_MATERIAL_DOES_NOT_EXPIRE'
    )
    logger.info("imported key material")



cmk = get_master_key(kms, MASTER_KEY_NAME)
if cmk:
    logger.info("found master key {0}".format(cmk))
else:
    logger.info("master key not found. creating key.")
    cmk = generate_external_master_key(kms)

import_key_material(kms, cmk)
