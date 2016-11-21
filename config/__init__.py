MASTER_KEY_NAME = "External_Master_Key"
ALIAS_PATTERN = "alias/{0}"
PLAINTEXT_KEY = "../key_material/PlaintextKeyMaterial.bin"
ENCRYPTED_KEY = "../key_material/EncryptedKeyMaterial.bin"
PUBLIC_KEY = "../key_material/public.key.bin"
PUBLIC_KEY_64 = PUBLIC_KEY + ".b64"


def get_master_key(client, key_alias):
    aliases = client.list_aliases()
    for alias in aliases['Aliases']:
        if alias['AliasName'] == ALIAS_PATTERN.format(key_alias):
            return alias['TargetKeyId']
    return False
