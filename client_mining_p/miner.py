import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof

def proof_of_work(last_proof):
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1
    print("Proof found: " + str(proof))
    return proof

def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))
        # TODO: When found, POST it to the server {"proof": new_proof}
        post_data = {"proof": new_proof}
        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        print(data)
        # # TODO: If the server responds with 'New Block Forged'
        if data.get('message') == 'New Block Forged':
        #     # add 1 to the number of coins mined and print it.  Otherwise,
            coins_mined += 1
        #     # print the message from the server.
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))