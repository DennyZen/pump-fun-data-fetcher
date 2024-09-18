import json
import asyncio
import atexit
from datetime import datetime
from loguru import logger
from websockets import connect
import aiosqlite
from solana.rpc.async_api import AsyncClient
#from solana.publickey import PublicKey
from solders.pubkey import Pubkey
from solana.rpc.types import TxOpts

# Solana WebSocket and RPC endpoints
SOLANA_WS_URL = "wss://api.mainnet-beta.solana.com"
ACCOUNTS_TO_FOLLOW = [
    "3eJkwFDZVB27emciij1oWUVodmFhFdnkpmzKHjDzH34o",
    "CPUvH6fYkpYBK5raccquTMNJAGc6eQ37VVqBgHq3hwjp",
    "7Gt57NfrPD82K8YpTsSijPB2tfdob7Hy1nU7C67P1J52",
    "3HYhQDQ9KmndBH1gMSSjY1QBKQ4UH5UYDYp4FXadHeA6",
    "JDaZYoxv5WvRtYDF5Yck5ZQgzXD5afbYRiekPwZ6kUo5", #fingers crossed        
    # Add more accounts as needed
]

DB_PATH = 'solana_events7.db'

# Configure logging
#logger.remove()
logger.add(f"solana_lana.log", rotation="1 day", compression="zip", level="TRACE", backtrace=True, diagnose=True)

# Initialize the database with event and transaction tables
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS account_events (
                               account TEXT,
                               lamports INTEGER,
                               owner TEXT,
                               rent_epoch INTEGER,
                               space INTEGER,
                               slot INTEGER,
                               timestamp TEXT
                           )''')
        await db.execute('''CREATE TABLE IF NOT EXISTS transactions (
                               signature TEXT PRIMARY KEY,
                               account TEXT,
                               slot INTEGER,
                               details TEXT,
                               timestamp TEXT
                           )''')
        await db.commit()

# Fetch recent transactions for a wallet using Solana Python SDK
async def fetch_transactions(client, account, limit=10, debug=False):
    if debug:
        logger.debug(f"Fetching confirmed transactions for account: {account}")
    
    try:
        # Fetch the transaction signatures
        result = await client.get_signatures_for_address(PublicKey(account), limit=limit) #shoould maintain list and limit
        if result['result']:
            if debug:
                logger.debug(f"Received transactions for {account}: {json.dumps(result['result'], indent=2)}")
                #else:
                logger.info(f"total {len(result['result'])} signatures") #finalized + list of errors (if any)
            return result['result']
        else:
            logger.error(f"No transactions found for {account}")
    except Exception as e:
        logger.error(f"Error fetching transactions for {account}: {e}")
    return None

# Save transaction details to the database
async def save_transaction_to_db(account, signature, slot, parsed_data, debug=False):
    async with aiosqlite.connect(DB_PATH) as db:
        timestamp = datetime.utcnow().isoformat()
        details = json.dumps(parsed_data)
        await db.execute('''INSERT OR IGNORE INTO transactions (signature, account, slot, details, timestamp)
                            VALUES (?, ?, ?, ?, ?)''', 
                         (signature, account, slot, details, timestamp))
        await db.commit()
    if debug:
        logger.debug(f"Saved transaction to database for signature: {signature}")

# Save account event details to the database
async def save_event_to_db(account, lp, slot, debug=False):
    async with aiosqlite.connect(DB_PATH) as db:
        timestamp = datetime.utcnow().isoformat()
        await db.execute('''INSERT INTO account_events (account, lamports, slot, timestamp)
                            VALUES (?, ?, ?, ?)''', 
                         (account, lp, slot, timestamp))
        await db.commit()
    if debug:
        logger.debug(f"Saved event to database for account: {account}")

# Subscribe to WebSocket events for specific accounts
async def listen_for_events(accounts, debug=False):
    async with connect(SOLANA_WS_URL) as websocket:
        client = AsyncClient("https://api.mainnet-beta.solana.com")
        subscription_ids = {}
        '''await websocket.send(json.dumps({
            "jsonrpc": "2.0", "id": 1, 
            "method": "getTransaction", 
            "params": ["5HbX6YFiQJsUhG1RM6YN8KNNY86rEpRJpG9WUWJmirAeiby5B6b6nH5qK43xctCxhecLKCmdKzuA1uFqFrLMfALg", {"encoding": "jsonParsed", "maxSupportedTransactionVersion":0} ]
            }))
        resp = await websocket.recv()
        #data = json.loads(resp)
        #client.get'''
        # Subscribe to each account, if there're many can be diff response.. fix see
        for account in accounts: #write an else statement
            await websocket.send(json.dumps({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "accountSubscribe",
                "params": [account, {"encoding": "jsonParsed"}]
            }))

            binding = await websocket.recv()
            data = json.loads(binding)
            if data and 'result' in data and data['result']:
                subscription_id = data['result']
                if debug:
                    logger.debug(f"Received message: {data}")
                data['wallet'] = account #, True, data['on']
                data['pp'] = 0
            
                subscription_ids[subscription_id] = data #account)
                logger.success(f"Subscribed to account: {account}, {subscription_id}")
            else:
                logger.warning(f'{data}') #here can be diff response

        async def unsubscribe():
            for subscription_id in subscription_ids:
                logger.info(f"Unsubscribing from subscription_id: {subscription_id}, {subscription_ids[subscription_id]['wallet']}")
                await websocket.send(json.dumps({
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "accountUnsubscribe",
                    "params": [account]
                }))
            await client.close()

        # Ensure unsubscribe on exit
        atexit.register(asyncio.run, unsubscribe())

        # Continuously listen to WebSocket events
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                if debug:
                    logger.debug(f"Received message: {data}")

                if 'method' in data and data['method'] == 'accountNotification': #todo: else...
                    account = data['params']['result']
                    subscription_id = data['params']['subscription']
                    slot = account['context']['slot']
                    event_data = account['value']
                    lamports = event_data['lamports']
                    wallet = subscription_ids[subscription_id]['wallet']
                    if 'pp' in subscription_ids[subscription_id]:
                        prev_price = lamports - subscription_ids[subscription_id]['pp'] 
                        subscription_ids[subscription_id]['pp'] = lamports
                        #if prev_price / 10**9 > lamports / 10**9 + 1:
                    else:
                        prev_price = 0
                        
                    msg=(f"Account balance update for {wallet}: {lamports/ 10**9}sol, prev_price_diff: {abs(prev_price)/10**9}sol") #\n{event_data}") #now n before the deal
                    if debug:
                        logger.critical(msg)
                    else:
                        print(f'{msg}') #wallet}: {lamports}') #todo prev state so pretend one at a time token and can ++ if deal>comsa

                    # Save the event in the database
                    await save_event_to_db(wallet, lamports, slot) #adjust cols
                    '''dont_fetch_transactions = True
                    if dont_fetch_transactions:
                        return

                    # Fetch transactions and log details
                    tx_data = await fetch_transactions(client, wallet, limit=5) #longer que +only new
                    if tx_data:
                        for tx in tx_data:
                            signature = tx['signature']
                            await save_transaction_to_db(wallet, signature, slot, tx) #add blocks?..'''

            except Exception as e:
                logger.error(f"Error in WebSocket listener: {e}")

# Main function to initialize the database and start listening
async def main():
    await init_db()
    await listen_for_events(ACCOUNTS_TO_FOLLOW)

if __name__ == "__main__":
    asyncio.run(main())
