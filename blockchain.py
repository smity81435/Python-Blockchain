# DOUGLAS SMITH
# Python Blockchain Example

MINIMG_REWARD = 10
GENESIS_BLOCK = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}

blockchain = [GENESIS_BLOCK]
open_transactions = []
owner = 'Douglas'
participants = {'Douglas'}


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_balance(participant):
    '''Returns the account balance of the participant.\n
    Arguments:\n
    :participant: Name of the participant.'''

    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]

    tx_sender.append(open_tx_sender)

    amt_sent = 0.0
    for tx in tx_sender:
        if len(tx) >= 1:
            amt_sent += tx[0]

    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]

    amt_rcvd = 0.0
    for tx in tx_recipient:
        if len(tx) > 0:
            amt_rcvd += tx[0]

    return amt_rcvd - amt_sent


def get_last_value():
    """ Returns the last value of the blockchain """

    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last value to the blockchain.

    Arguments: \n
        :sender: sender of the coins \n
        :recipient: Receiver of the coins\n
        :amount: Amount of coins (default[1.0])
    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
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
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINIMG_REWARD
    }

    open_transactions.append(reward_transaction)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }

    blockchain.append(block)
    return True


def get_transaction_details():
    """ Returns the new user input transaction amount as a float. """
    tx_recipient = input("Name of the recipient: ")
    tx_amount = float(input("Amount of coins transferred: "))
    return (tx_recipient, tx_amount)


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
    return True


def print_participants():
    print('\n')
    print('PARTICIPANTS: ')
    print('-'*10)

    for name in participants:
        print('Name: '+name)

    print('-'*10)
    print('\n')


def main():
    waiting_for_input = True
    while waiting_for_input:
        print('Please Choose: ')
        print('-'*10)
        print('1: Add a new transaction')
        print('2: Mine a new block')
        print('3: Output the blockchain')
        print('4: Output the participants')
        print('5: Simulate Hack')
        print('6: Quit')
        print('-'*10)

        choice = get_user_choice()
        if choice == 1:
            tx_data = get_transaction_details()
            recipient, amount = tx_data
            if add_transaction(recipient, amount=amount):
                print('-'*10)
                print('Transaction Added to Blockchain!!')
                print('-'*10)
            else:
                print('Transaction Failed')
        elif choice == 2:
            if mine_block():
                open_transactions = []
        elif choice == 3:
            # print the chain
            print_chain()
        elif choice == 4:
            print_participants()
        elif choice == 5:
            # Hack the blockchain
            if len(blockchain) >= 1:
                blockchain[0] = {
                    'previous_hash': '',
                    'index': 0,
                    'transactions': [{'sender': 'Chris', 'recipient': 'Doug', 'amount': 500.0}]
                }
        elif choice == 6:
            waiting_for_input = False
        else:
            print('-'*10)
            print('Unrecognized command!')
            print('-'*10)
        if not verify_chain():
            print('Invalid Blockchain!')
            break
        print('Funds Available: ')
        print(get_balance('Douglas'))
    else:
        print('Ending program.')


main()
