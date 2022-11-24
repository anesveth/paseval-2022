import hashlib


def encode_password(str_password):
    '''
    Encode password to sha1 so as to send it to the HaveIbeenPawned API
    '''
    # Strings must be encoded before hashing
    enc = hashlib.sha1(str_password.encode('utf-8'))
    hash_to_send = enc.hexdigest()
    return hash_to_send
