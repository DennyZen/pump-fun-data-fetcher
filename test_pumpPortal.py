import asyncio
import websockets
import json

from google_sheets import write_to_google_sheets,  big_last_row

wallet_addresses = [
    "DS2KkjMazkU5rN6E2KMMzTS5ct8aQVP2ruBf57K4c1FF",
    "4tK7RdcseCvPxAQZiv7iAzyqawedEe16dZb1FZ39zarj",
    "8TKbC2hE5RwnXUNe2b2a6e5UmRdxPTGS5LX6B2RWAv83",
    "G5vWA8juZKcEcNBq6noaYC25kNEy1f5NWY9aaBHF8Cno",
    "AYgZ8C6P11c8iTCj2YyANT9Xok6XUm7iZ7BCeR7fW3XL",
    "CWvdyvKHEu8Z6QqGraJT3sLPyp9bJfFhoXcxUYRKC8ou",
    "2RssnB7hcrnBEx55hXMKT1E7gN27g9ecQFbbCc5Zjajq",
    "DY5Ej41PGDWsDoxMJPbrewTjzyVPLmm5kNL5Bsw3mMVX",
    "4ADFwrmsrdSVUx8cp7mVtcynvM3hFcdkBZk4vi83KnrA",
    "4K1QY4aSGveSZ5UUpeG6LP6JsqkSZPvBMo3JD2YTmCCE",
    "nAxHm1ZmiSbu9kPM4orssuRRUqCJGWE4rzEtYpa5yTp",
    "GQWLRHtR18vy8myoHkgc9SMcSzwUdBjJ816vehSBwcis",
    "39PcuE9MBnW4FnqcDJYiy4ppRApdDq4XN4bfksG2nEuP",
    "BWQMaBZXLTH3RVvRZjwKhQFTahmEtZiSiyWkA94F4oHu",
    "4PkUrVUp99BwePxDvvgoGVYZM213GyE9VR8Z5235sbVe",
    "5ePaQ8YreTMQbNoBwiFe6mbvBLBYoGFek3U3pC8TVVsw",
    "JDZyJqZh6vwqnCeGBXymXPFkMTqDNAGJnm7rz1t6BTnQ",
    "6bKUguaAgYYbxwvzg7ge4vNTHtrVTmKBSfJRWVvNwAPr",
    "Ec4BAURantJU6P2yn7HQLxZq9bUo4ZFmc5DAJhVMM1oc",
    "sEVggxf69nwprkgCPpLMq5i4eAYxYutxCLBiLn5EWRq",
    "Haq5TB66joFhjKGGSBi6Sdk3Rh9xX4We6wCePGV5uArP",
    "Bq2RWav5LtfnAs8refzrYjfroDGK9vjYULmTqJX7yXfJ",
    "5QemTzE4eBsfpN9XjTHmQLVwKjDkdUjcAJKEL4JW9Vgv",
    "gEwDSjhP1xJFUwiaZDjTNvaTCtKhBjybR2nxPrHzkGc",
    "H1iBiJj595JhzeQaeudJrfBvMSRKiLNC2NQytrbfW3hU"
]
wallet_addresses+=['4mH6ENXnLCLf98BCz5BVHfUHDvV6c4wKeDLjAoMxu5Ja','F46fkvycu8cRRB7Z2pnkkCug7a2m1crSBGdjPoCsHvNA', 'A719nD9SkNrG2EQP6CLQFURVKcqfqrT6AJSN3MnR6HSB']
# From Ray Wallet tracker
CA = '5FMjMuiAdgwF3REQogMqrdLRBF9pKs5wfJ9hW71Fpump'

async def subscribe(payload):
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        if isinstance(payload, list):
            for item in payload:
                await websocket.send(json.dumps(item))
        elif isinstance(payload, dict):
            await websocket.send(json.dumps(payload))
        else:
            raise TypeError("payload must be a list or a msg_dict")
        
        
        async for message in websocket:
            msg_dict = json.loads(message)
            print(msg_dict)

            if msg_dict.get('message')=='Successfully subscribed to keys.':
                big_last_row()
                msg = 'subscribed to Wallets: '+', '.join(wallet_addresses)
                print(msg)
                write_to_google_sheets([[msg]])   #  [['value2','value1']]
            elif msg_dict.get('message')=='Successfully subscribed to token creation events.':
                big_last_row(list_name='New Coins')
                msg = 'Successfully subscribed to token creation events:'
                write_to_google_sheets([[msg]], list_name='New Coins')
            elif msg_dict.get('txType')=='create':
                    # {'signature': '23eCp3myeTYDP8kLXX3qPU5kQaNwKp1xVBu5mS6yht2hqzt3Zc3wJYrEJnp3fQPs5KTkgeYE7oicyqSVjpMRFj6F', 'mint': '6MniZfAeRg1RRHCddsYQH9mdxREW22CzezxKM2ukFDfp', 'traderPublicKey': '3mxcUNwJNfRajSPdD3yXsuomHtDUfwQSjB17XethgkVn', 'txType': 'create', 'initialBuy': 56259633.607075, 'bondingCurveKey': 'GhKTK26NQt4uQ7hVePxZjantgQZpa4yNDkqCtoeRSVMA', 'vTokensInBondingCurve': 1016740366.392925, 'vSolInBondingCurve': 31.659999999999993, 'marketCapSol': 31.1387263125194, 'name': 'up', 'symbol': 'up', 'uri': 'https://ipfs.io/ipfs/QmW1uhY2xbToS99GiJxqGS7xuDkx5MRdznE12sRucNL6Jn'}
                    msg = [msg_dict["name"], msg_dict["symbol"], msg_dict["initialBuy"], msg_dict['marketCapSol']]
                    #print(f'subscribeNewToken !  {msg}')
                    write_to_google_sheets([msg], list_name='New Coins')
            elif msg_dict.get('txType')!='create':
                msg = [msg_dict['mint'], msg_dict['txType'], msg_dict['tokenAmount'], msg_dict['newTokenBalance'], msg_dict['marketCapSol']]
                print(msg)
                write_to_google_sheets([msg])   #  [['value2','value1']]

payload2 = {
            "method": "subscribeNewToken",
        }
payload = {
            "method": "subscribeTokenTrade",
            "keys": [CA]  # array of token CAs to watch
        }
payload3 = {
        "method": "subscribeAccountTrade",
        "keys": wallet_addresses  # array of accounts to watch
    }
payload = [payload2, payload3]

asyncio.get_event_loop().run_until_complete(subscribe(payload))