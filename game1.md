# The Offline Blockchain

We will split into 5 groups of:

- 3 verifiers and recorders
- 1 network and attackers
- 2 senders

## Materials needed
- Pen
- Paper
- A 6 sided [dice](https://www.random.org/dice/?num=1)


# Senders
The senders send transactions to the network.
- Write transactions on peices of paper, fold them and pass them to members of the network group.
```js
id:  ...
to:  ...
from:  ...
amount:  ...
data:  ...
verification_information: ...
```
- Senders can send a maximum of 10 coins per transaction
- They must also record all that you send
- Sender groups start with 100 coins each
- Sender groups will decide what initial accounts have any coins


## Sender Constraints
They can only communicate verbally with their own group and the Network group.


## Senders Goals

The senders goals are quite straight forward.
- Each group must send over 100 coins in total to the other sender group.
- Each group must also include the names of their group members in different transactions, so that they are recorded as e.g. `name: M. Mifty, group: Sender-1` 

# Network Team and Attackers

The network takes the transactions from the both senders groups, reads them and shows them to each of the *verifiers and recorder* group. 

The attackers are allowed to take the transaction paper out of the room (or otherwise hide it from view). In addition the attackers can:

1. write on the transaction paper
2. copy the transactions
3. create their own transactions
4. delay transactions by up to two minutes
5. reorder transactions

## Network Team Constraints

Before the game begins, only half the group is allowed to make attacker actions. The members that are not attackers may leave the room, but may not manipulate the transactions in the ways  suggested above. 
> You can swap at half time if you like. 

You must elect a recorder to record all the manu

## Network Team Goals

The Network Team must deliver all transactions. In addition, they are aiming to achieve a couple of goals:

- Get the Recorder Team to accept  


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










