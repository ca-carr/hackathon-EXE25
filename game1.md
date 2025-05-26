# Game 1, The Offline Blockchain

## Game Overview
This game simulates a blockchain network without computers, to get to the fundamental concepts through thinking about the actual interactions.

## Setup

We will split into 5 groups of:
- 3 Verifier Groups (including Recorders)
- 1 Network Group (inluding Attackers)
- 2 Sender Groups

## Materials needed
- Pen(s)
- Paper
- A 6 sided [dice](https://www.random.org/dice/?num=1)
- Timer 

# Initial Setup
- Decide on your groups, who will be Sender group, who will be the Verifier group and the Network group.
- Each Sender group starts with 100 coins, assigned somehow (you decide)
- Create initial account balances on a "genesis block" (an initial state)
- All Verifier groups need to be aware of this state somehow (you decide)
- **Crucial** before the game begins, all groups together decide on how the blockchain system will work

# Senders
The senders send transactions to the network.
- Write transactions on peices of paper, fold them and pass them to members of the Network group. 
- You can decide on the transaction format, below is two examples to get you started.
```js
# example_1
id:  ...
to:  ...
from:  ...
amount:  ...
data:  ...
verification_information: ...
```
```js
# example_2
transaction #: ___
from: ___ (account)
to: ___ (account)
amount: ___ coins
timestamp: ___
nonce: ___ (random number)
signature: ___ (unique mark)
```


- Senders can send a maximum of 10 coins per transaction
- They must also record all that you send
- Sender groups start with 100 coins each, as per setup
- Sender groups will decide what initial accounts have any coins


## Sender Constraints
They can only communicate verbally with their own group and the Network group. They cannot speak with the Verificaction groups.


## Senders Goals

The senders goals are quite straight forward.
- Each group must send over 100 coins in total to the other sender group.
- Each group must also include the names of their group members in different transactions, so that they are recorded as e.g. `name: M. Mifty, group: Sender-1` 

# Network and Attackers

- The Network group also contains the attackers. 
- The network takes the transactions from the both senders groups, reads them and shows them to each of the Verifier group. 

The attackers are allowed to take the transaction paper out of the room (or otherwise hide it from view). In addition the attackers can:

1. write on the transaction paper
2. copy the transactions
3. create their own transactions (forgery)
4. delay transactions by up to two minutes
5. reorder transactions

## Network Team Constraints

Before the game begins, only half the group is allowed to make attacker actions. The members that are not attackers may leave the room, but may not manipulate the transactions in the ways the attackers can. 
> You can swap at half time if you like. 

- You must ensure you do not tell any other group who is an attacker and who is not. In addition, the Network group must act together.
- You must elect a recorder to record all the transactions that you see, and all of the attacker manipulated transactions.

## Network Team Goals

The first goal of the Network Team is to deliver all transaction.

In addition, the attacker members are aiming to achieve a couple of goals:

- Get the Recorder Team(s) to accept a double-spend
- Get the Recorder Team(s) to accept a forgery
- Make it so the ledger between the different recorder teams does not match
-  



---

# Verifiers and Recorders

This group forms the consensus and agreement layer of the blockchain.

### Responsibilities
- Verify each transaction
- Accept or Reject transactions
- Append a transaction to your ledger
    - When a new transaction is appended, roll the dice, on a 6 you have made a block
    - Underscore transactions and share the block with the other groups
    - They must copy your ledger as it is and discard their own (though they may keep any transactions that they have not seen or have not been duplicated.)



## Recorder Team Goals

- Create more blocks that the other recorder teams.
- Detect and flag any tampered or invalid transactions.





# Game End and Win Conditions
The game ends after 20 minutes.


Winning Criteria

Attackers **Super Win** Condition:
- All blocks / overwhelming created contain tampered or invalid transactions created by the attackers **and** the following win condition applies

Attackers **Win** condition:
- All transactions are delivered to all Recorder Teams on the network
- A forged transaction is included
- Cause inconsistency between recorded ledgers
- Caused invalid or double payment


Recorders **Super Win** Condition: 
- More blocks created than other teams and
- No block contains tampered or invalid transactions created by the attackers.

- Senders **Win** if:
- They send 100+ coins to the opposing team (or more)
- All transactions are accepted into the final blockchain.
- Each sender’s name appears at least once in accepted transactions.










