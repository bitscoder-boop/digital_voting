from fastapi import FastAPI
from architecture import Blockchain
import time


app = FastAPI()
blockchain = Blockchain()
blockchain.create_genesis_block()

# the address to other participating members of the network
nodes = set()

@app.post('/new_transcation')
def new_transcation(voter_id: str, candidate: str):
    data = {'voter': voter_id, 'candidate': candidate, 'timestamp': time.time()}
    blockchain.add_new_transaction(data)
    return "Success"


@app.post("/register_node")
def register_node(node_address: str):
    a = nodes.add(node_address)
    if a:
        return {"success": True}
    return {"succes": False}


@app.get("/mine")
def mine_unconfirmed_tranctions():
    result = blockchain.mine()
    return result
    # if not result:
    #     return "No transactions to mine"
    # else:
    #     return "Mined succesfully"


@app.get('/get_chain')
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return {"length": len(chain_data), "chain": chain_data}


@app.get('/pending_transaction')
def get_pending_transactions():
    return {'data': blockchain.unconfirmed_transctions}
