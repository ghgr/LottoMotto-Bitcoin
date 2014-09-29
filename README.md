This project is a blockchain-based, provably-fair, low-latency lottery for Bitcoin.

The jackpot is given to the last address after X blocks (default: 3) without transactions.

To avoid DOS attacks only transaction with fee are considered.


The project is composed of two parts:


1) Web Frontend. All javascript, no PHP (you can even host it in Dropbox). It makes requests to Blockchain.info API (through corsproxy, since somehow I cannot call it directly [CORS]).

2) Python core. It can (and should, really!) run in a separated computer far away from the frontend. This part uses Electrum/Bitcoind/... and handles payments.



There is a Gateway address. This address is ignored in the web frontend, and is used to add/remove funds from the lotto address (and don't confuse the user, making them think it was a player)


Donations: 1GhgraoJ3LqpMF9CDEc1UL3q5EkXZyUdHH
