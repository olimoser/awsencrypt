from Crypto.Cipher import AES
import hashlib

ec_suite = AES.new('0123456789abcdef0123456789abcdef', AES.MODE_CBC, 'ThisIsIV12345678')
cipher_text = ec_suite.encrypt('This is a secret message. 123456')

print cipher_text

dc_suite = AES.new('0123456789abcdef0123456789abcdef', AES.MODE_CBC, 'ThisIsIV12345678')
plain_text = dc_suite.decrypt(cipher_text)

print plain_text


pw = "test1"
key = hashlib.sha256(pw).digest()
print key

