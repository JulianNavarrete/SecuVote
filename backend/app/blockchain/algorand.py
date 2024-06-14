from algosdk.v2client import algod
from algosdk import transaction, mnemonic


algod_address = "https://testnet-api.algonode.cloud"

# free service does not require tokens
algod_token = ""

# Initialize the algod client
algod_client = algod.AlgodClient(algod_token, algod_address)

# Get the node status
try:
    status = algod_client.status()
    print("Node status:", status)
except Exception as e:
    print(f"Failed to get node status: {e}")


# Function to create an Algorand transaction
def create_algorand_txn(sender_address, recipient_address):
    # print("Sender address:", sender_address)
    # print("Recipient address:", recipient_address)
    params = algod_client.suggested_params()
    txn = transaction.PaymentTxn(sender_address, params, recipient_address, 0, None, params.fee)
    return txn


# Function to sign an Algorand transaction
def sign_algorand_txn(txn, sender_mnemonic):
    sender_private_key = mnemonic.to_private_key(sender_mnemonic)
    signed_txn = txn.sign(sender_private_key)
    return signed_txn


# Function to send an Algorand transaction
def send_algorand_txn(signed_txn):
    txid = algod_client.send_transaction(signed_txn)
    return txid

