from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv


filename = '/Users/f22daniel/PycharmProjects/Griraffe/smart_contract_development/Web3_SimpleStorage/SimpleStorage.sol'
with open(filename, "r") as file:
    simple_storage_file = file.read()

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
)
# print(compiled_sol)

with open("/Users/f22daniel/PycharmProjects/Griraffe/smart_contract_development/Web3_SimpleStorage/compiled_code.json", "w") as file:
    json.dump(compiled_sol, file, indent=2)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
# print('')
# print(bytecode)
# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
# print('')
# print(abi)

# for connecting to Ganache
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/815e996eff9c4caa8cfe1349781148b6"))
chain_id = 4
my_address = "0x7F753e034A7ed1D423e7A22aC2dbe92B28650Af7"
private_key = '0x414c8f72c726144b3ccf292077ad2757f1268ef120316c51b68836ff4aff8cfe'
print(os.getenv("PRIVATE_KEY"))

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print('')
print(nonce)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": nonce})
# print('checkpoint')
# print('')
print(transaction)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print('Deploying contract....')
# print(signed_txn)
# Send this signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print('Deployed!!!')
# Working with the contract, you always need:
    # 1. Contract Address
    # 2. Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value
# Transact -> Actually make a state change
print(simple_storage.functions.retrieve().call())
print('Updating Contract....')
# 1. Build a transaction
store_transaction = simple_storage.functions.store(15).buildTransaction({'chainId': chain_id, "gasPrice": w3.eth.gas_price, 'from': my_address, 'nonce': nonce + 1})
# print(simple_storage.functions.store(15).call())
# 2. Sign a transaction
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
# 3. Send a transaction
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
# 4. Waiting for finished transaction
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print('Contract updated!!!')
print(simple_storage.functions.retrieve().call())
''''''
