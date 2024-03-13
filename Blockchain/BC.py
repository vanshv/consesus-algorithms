import Blockchain.B as B
import json

class Blockchain:
    def __init__(self):
        self.chain = [B.Block().genesis()]
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        
    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = B.Block().create_block(last_block, data)
        self.chain.append(new_block)
        return new_block
    
    def isValid(chain):
        if str(chain[0]) != str(B.Block().genesis()):
            return False

        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            if current_block.last_hash != previous_block.hash:
                return False

            if current_block.hash != B.Block().block_hash(current_block):
                return False

        return True
    
    def replace_chain(self, new_chain):
        if len(new_chain) <= len(self.chain):
            print("Received chain is not longer than the current chain.")
            return

        if not self.is_valid_chain(new_chain):
            print("Received chain is invalid.")
            return

        print("Replacing the current chain with the new chain.")
        self.chain = new_chain