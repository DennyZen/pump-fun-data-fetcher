import asyncio
import websockets
import json

CA = '5FMjMuiAdgwF3REQogMqrdLRBF9pKs5wfJ9hW71Fpump'
async def subscribe():
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        
        # Subscribing to token creation events
        payload = {
            "method": "subscribeNewToken",
        }

        # Subscribing to trades made by accounts
        # payload = {
        #     "method": "subscribeAccountTrade",
        #     "keys": ["AArPXm8JatJiuyEffuC1un2Sc835SULa4uQqDcaGpAjV"]  # array of accounts to watch
        # }

        # Subscribing to trades on tokens
        payload = {
            "method": "subscribeTokenTrade",
            "keys": [CA]  # array of token CAs to watch
        }
        await websocket.send(json.dumps(payload))
        
        async for message in websocket:
            print(json.loads(message))

    # Run the subscribe function
asyncio.get_event_loop().run_until_complete(subscribe())