# Forked from Auction Algorand demo example : https://github.com/algorand/auction-demo

from algosdk.transaction import PaymentTxn
from resr.util import (
    getBalances,
)
from resr.testing.setup import getAlgodClient
from resr.testing.resources import (
    getTemporaryAccount,
    createDummyAsset,
)
from algosdk import account, mnemonic
from algosdk import transaction


def create_payment_transaction(escrow_address, params, receiver, amount):
    return PaymentTxn(escrow_address, params, receiver, amount)


def payout_Test():

    private_key, address = account.generate_account()
    client = getAlgodClient()

    print("Generating Demo Users ...")
    user = getTemporaryAccount(client)
    green_manufact = getTemporaryAccount(client)
    legacy_manufact = getTemporaryAccount(client)
    treasury = getTemporaryAccount(client)

    print("Treasury account :", treasury.getAddress())
    print("Bob (User account):", user.getAddress())
    print("Tesla (Green manufacturer account):", green_manufact.getAddress())
    print("Shell (Legacy manufacturer account)", legacy_manufact.getAddress(), "\n")

    print("Treasury's balances:", getBalances(client, treasury.getAddress()))
    print("Bob's balances:", getBalances(client, user.getAddress()))
    print("Tesla's balances:", getBalances(client, green_manufact.getAddress()))
    print("Shell's balances:", getBalances(client, legacy_manufact.getAddress()), "\n")

    print("Shell is sending sensor data ...")
    dataAmount = 2
    dataID = createDummyAsset(client, dataAmount, legacy_manufact)
    print("The data ID is", dataID)
    amount = dataAmount * 10000000
    params = client.suggested_params()
    print("Shell is sending Carbon tax to treasury ...")
    pay = PaymentTxn(legacy_manufact.getAddress(), params, treasury.getAddress(), int(amount))
    signed_txn = pay.sign(legacy_manufact.getPrivateKey())
    txid = client.send_transaction(signed_txn)
    print("Successfully submitted transaction with txID: {}".format(txid))
    txn_result = transaction.wait_for_confirmation(client, txid, 4)

    print("Bob is sending sensor data ...")
    dataAmount = 1
    dataID = createDummyAsset(client, dataAmount, user)
    print("The data ID is", dataID)
    amount = dataAmount * getBalances(client, treasury.getAddress())[0] * 0.01  # temporary formula : 1% of treasury for each unit of data shared
    params = client.suggested_params()
    print("Bob is claiming his data sharing insentive ...")
    pay = PaymentTxn(treasury.getAddress(), params, user.getAddress(), int(amount))
    signed_txn = pay.sign(treasury.getPrivateKey())
    txid = client.send_transaction(signed_txn)
    print("Successfully submitted transaction with txID: {}".format(txid))
    txn_result = transaction.wait_for_confirmation(client, txid, 4)

    print("Tesla is sending sensor data ...")
    dataAmount = 3
    dataID = createDummyAsset(client, dataAmount, green_manufact)
    print("The data ID is", dataID)
    amount = dataAmount * getBalances(client, treasury.getAddress())[0] * 0.02  # temporary formula : 2% of treasury for each unit of data shared
    params = client.suggested_params()
    print("Tesla is receiving benefits for being carbon neutral ...")
    pay = PaymentTxn(treasury.getAddress(), params, green_manufact.getAddress(), int(amount))
    signed_txn = pay.sign(treasury.getPrivateKey())
    txid = client.send_transaction(signed_txn)
    print("Successfully submitted transaction with txID: {}".format(txid))
    txn_result = transaction.wait_for_confirmation(client, txid, 4)

    print("\nTreasury's balances:", getBalances(client, treasury.getAddress()))
    print("Bob's balances:", getBalances(client, user.getAddress()))
    print("Tesla's balances:", getBalances(client, green_manufact.getAddress()))
    print("Shell's balances:", getBalances(client, legacy_manufact.getAddress()))


payout_Test()
