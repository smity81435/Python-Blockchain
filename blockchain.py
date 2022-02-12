# DOUGLAS SMITH
# Python Blockchain Example
from functools import reduce
import hashlib as hl
import json
from collections import OrderedDict

MINING_REWARD = 10
GENESIS_BLOCK = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}

blockchain = [GENESIS_BLOCK]
open_transactions = []
owner = 'Douglas'
participants = {'Douglas'}


def hash_block(block):
    '''Hashes a given block. \n
    :block: Block to be hashed {previous_hash:str, index: int, transactions:[transaction]}
    '''
    return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()


def valid_proof(transactions, last_hash, proof):

    guess = f'{transactions}{last_hash}{proof}'
    encoded_guess = guess.encode()
    guess_hash = hl.sha256(encoded_guess).hexdigest()
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    '''Returns the account balance of the participant.\n
    Arguments:\n
    :participant: Name of the participant.'''

    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]

    tx_sender.append(open_tx_sender)

    amt_sent = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum+0, tx_sender, 0)

    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]

    amt_rcvd = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum+0, tx_recipient, 0)

    return amt_rcvd - amt_sent


def get_last_value():
    """ Returns the last value of the blockchain """

    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    '''Verifies the sender has enough in wallet to make transaction.\n
    :transaction: Transaction details {sender: str, recipient: str, amount: float}'''
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last value to the blockchain.

    Arguments: \n
        :sender: sender of the coins \n
        :recipient: Receiver of the coins\n
        :amount: Amount of coins (default[1.0])
    """

    transaction = OrderedDict(
        [('sender', sender),
         ('recipient', recipient),
         ('amount', amount)])

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    else:
        print('Not enough funds!!!')
        return False


def mine_block():
    ''' Creates a new block '''

    global open_transactions
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    proof = proof_of_work()

    reward_transaction = OrderedDict([('sender', 'MINING'),
                                      ('recipient', owner),
                                      ('amount', MINING_REWARD)])

    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }

    blockchain.append(block)
    open_transactions = []

    return True


def get_transaction_details():
    """ Returns the new user input transaction amount as a float. """

    recipient = input("Name of the recipient: ")
    amount = float(input("Amount of coins transferred: "))
    return (recipient, amount)


def get_user_choice():
    ''' Asks user for input. '''

    return int(input('Your choice: '))


def print_chain():
    ''' Prints each block in the chain '''

    for block in blockchain:
        print('Block:')
        print(block)


def verify_chain():
    ''' Verfies the integrity of the chain '''

    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            return False
    return True


def print_participants():
    '''Prints a list of participants.'''

    print('\n')
    print('PARTICIPANTS: ')
    print('-'*10)
    for name in participants:
        print('Name: '+name)
    print('-'*10)
    print('\n')


def clean_print(value):
    '''Prints a value with formatting'''

    print('-'*10)
    print(value)
    print('-'*10)


def verify_transactions():
    ''' Verifies all transactions in the unmined block.'''

    return all([verify_transaction(tx) for tx in open_transactions])


def main():
    waiting_for_input = True
    while waiting_for_input:
        print('Please Choose: ')
        print('-'*10)
        print('1: Add a new transaction')
        print('2: Mine a new block')
        print('3: Output the blockchain')
        print('4: Output the participants')
        print('5: Check transaction validity')
        print('6: Simulate Hack')
        print('7: Quit')
        print('-'*10)

        choice = get_user_choice()
        if choice == 1:
            tx_data = get_transaction_details()
            recipient, amount = tx_data
            if add_transaction(recipient, amount=amount):
                clean_print('Transaction Added to Blockchain!!')
            else:
                clean_print('Transaction Failed')
        elif choice == 2:
            if mine_block():
                clean_print("Block Mined!")
            else:
                clean_print("Unable to mine block")
        elif choice == 3:
            # print the chain
            print_chain()
        elif choice == 4:
            print_participants()
        elif choice == 5:
            if verify_transactions():
                clean_print('All transactions are valid')
            else:
                clean_print('Invalid transaction found')
        elif choice == 6:
            # Hack the blockchain
            if len(blockchain) >= 1:
                blockchain[0] = {
                    'previous_hash': '',
                    'index': 0,
                    'transactions': [{'sender': 'Chris', 'recipient': 'Doug', 'amount': 500.0}]
                }
        elif choice == 7:
            waiting_for_input = False
        else:
            clean_print('Unrecognized command!')
        if not verify_chain():
            clean_print('Invalid Blockchain!')
            break
        print('*'*20)
        print('Funds Available: ')
        print('Balance of {}: {:6.2f}'.format(
            'Douglas', get_balance('Douglas')))
        print('*'*20)
    else:
        clean_print('Ending program.')


main()
