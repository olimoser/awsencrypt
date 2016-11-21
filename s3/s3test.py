from __future__ import print_function
import config
from session import *

FILE = "./plaintext.txt"

aws_master_key = config.get_master_key(kms, config.MASTER_KEY_NAME)

data_key_response = kms.generate_data_key(KeyId=aws_master_key, KeySpec='AES_256')
plaintext_key = data_key_response['Plaintext']
ciphered_key = data_key_response['CiphertextBlob']

print(data_key_response)

print(kms.generate_random(NumberOfBytes=256))
