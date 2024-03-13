import os
from flask import Flask, jsonify, request, redirect
import Blockchain.BC as BC
import json
import Blockchain.B as B

HTTP_PORT = int(os.environ.get('HTTP_PORT', 3001))
app = Flask(__name__)
blockchain = BC.Blockchain()

@app.route('/blocks', methods=['GET'])
def get_blocks():
    return json.dumps([bl.__dict__ for bl in blockchain.chain])

@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()['data']
    print("hi", data)
    new_block = blockchain.add_block(data)
    print(f"New block added: {str(new_block)}")
    return redirect('/blocks')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=HTTP_PORT)