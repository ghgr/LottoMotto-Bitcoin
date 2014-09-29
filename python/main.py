BOUNTY=10
MIN_CONFIRMATIONS=3
TICKET_PRICE=0.01
LOTTO_ADDRESS="1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp"
GATEWAY_ADDRESS="1GatewAy"
MIN_FEE=0.0001

import random,time,json

def getTxList(address):
	print "Getting txlist from",address
	f=open("txs_received.json")
	data=json.loads(f.read())
	f.close()
	return data['txs']

def getSumOutputsToAddress(tx,address):
	sum_outputs=0
	for o in tx['out']:
		if o['addr']==address:
			sum_outputs+=o['value']
	sum_outputs*=1e-8
	print "Enviado=",sum_outputs
	return sum_outputs

def getConfirmationsOfTransaction(tx):
	f=open("last_block.json")
	data2=json.loads(f.read())
	f.close()
	current_block = data2['data']['blocks'][0]['height']
	n_confirmations=current_block-tx['block_height']+1
	print "This transaction has",n_confirmations,"confirmations"
	return n_confirmations

def payToAddress(qty,address):
	print "PAYING",qty,"to",address,"!"

def notePayment(tx):
	#Payments are defined for block AND address
	w=open("payed.txt",'a')
	w.write(tx['hash']+",\n")
	w.flush()
	w.close()

def checkIfPayed(tx):
	open("payed.txt", "a").close()
	f=open("payed.txt")
	checks=0
	for line in f:
		tx_tmp=line.split(',')
		if tx_tmp[0]==tx['hash']:
			f.close()
			return True
	f.close()
	return False

def getTxFee(tx):
	sum_inputs=0
	for inp in tx['inputs']:
		sum_inputs+=inp['prev_out']['value']
	sum_outputs=0
	for out in tx['out']:
		sum_outputs+=out['value']
	f = (sum_inputs-sum_outputs)*1e-8
	print "Getting fee","=",f
	return f

# START AUTOMATON

def state_getTxIterator():
	global CURRENT_STATE
	global txs_it
	txs_it=iter(getTxList(LOTTO_ADDRESS))
	CURRENT_STATE=state_getNextTx
	
def state_getNextTx():
        global CURRENT_STATE
	global tx
	tx=txs_it.next()
	CURRENT_STATE=state_isAmountRight

def state_isAmountRight():
        global CURRENT_STATE
	global TICKET_PRICE
	qty=getSumOutputsToAddress(tx,LOTTO_ADDRESS)
	if qty>=TICKET_PRICE:
		print "Good qty, check confirmations..."
		CURRENT_STATE=state_areConfirmationsRight
	else:
		print "BAD QTY, ignoring..."
		CURRENT_STATE=state_getNextTx

def state_areConfirmationsRight():
        global CURRENT_STATE
	global MIN_CONFIRMATIONS
	n_confirmations=getConfirmationsOfTransaction(tx)
	if n_confirmations>=MIN_CONFIRMATIONS:
		print "Confirmations OK, check if payed..."
		CURRENT_STATE=state_isAlreadyPayed
	else:
		print "Not confirmed yet, check fee..."
		CURRENT_STATE=state_checkFee

def state_checkFee():
	global CURRENT_STATE
	global MIN_FEE
	fee = getTxFee(tx)
	if fee>=MIN_FEE:
		print "Fee OK, consider it..."
		#CURRENT_STATE=state_wait
		print "NOTE:BYPASSING WAIT TO TEST, GETTING NEXT TX"
		CURRENT_STATE=state_getNextTx
	else:
		print "Not enough fee, probably attack..."
		CURRENT_STATE=state_getNextTx

def state_isAlreadyPayed():
        global CURRENT_STATE
	global tx
	if checkIfPayed(tx):
		print "Already payed, todo en orden (no need to continue)..."
		CURRENT_STATE=state_wait
	else:
		CURRENT_STATE=state_notePayment

def state_notePayment():
	global CURRENT_STATE
	global tx
	print "Noting payment..."
	notePayment(tx)	
	CURRENT_STATE=state_pay

def state_pay():
        global CURRENT_STATE
	print "Payed!"
	CURRENT_STATE=state_wait

def state_wait():
	global CURRENT_STATE
	raw_input("Waiting...\n-------------------------\n")
#	print "Waiting..."
#	time.sleep(1000)
	CURRENT_STATE = state_getTxIterator

if __name__=="__main__":
	import time
	print "Bounty is",BOUNTY
	print "Lim confirmations is",MIN_CONFIRMATIONS
	print "Ticket price is",TICKET_PRICE
	print "Lotto address",LOTTO_ADDRESS
	print "Gateway address",GATEWAY_ADDRESS

	CURRENT_STATE=state_getTxIterator
	print "***** MAIN LOOP ********"
	while True:
		CURRENT_STATE()
