import hashlib as hl
import json


def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    '''Hashes a given block. \n
    :block: Block to be hashed {previous_hash:str, index: int, transactions:[transaction]}
    '''
    return hash_string_256(json.dumps(block, sort_keys=True).encode())
