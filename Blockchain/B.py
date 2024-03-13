import hashlib
import datetime
import json

class Block:
    def __init__(self, timestamp=None, last_hash=None, hash=None, data=None, validator=None, signature=None):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.validator = validator
        self.signature = signature

    def __str__(self):
        block_dict = {
            'timestamp': self.timestamp,
            'last_hash': self.last_hash,
            'hash': self.hash,
            'data': self.data,
            'validator': self.validator,
            'signature': self.signature
        }
        return json.dumps(block_dict, indent=4)
            
    @staticmethod
    def genesis():
        return Block("genesis time", "----", "genesis-hash", [], None, None)
    
    @staticmethod
    def hash(timestamp, last_hash, data):
        data_string = f"{timestamp}{last_hash}{str(data)}"
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    @staticmethod
    def create_block(last_block, data):
        hash = ''
        timestamp = int(datetime.datetime.now().timestamp())
        last_hash = last_block.hash

        hash = Block.hash(timestamp, last_hash, data)
        return Block(timestamp, last_hash, hash, data)

    @staticmethod
    def block_hash(block):
        timestamp = block.timestamp
        last_hash = block.last_hash
        data = block.data
        return Block.hash(timestamp, last_hash, data)