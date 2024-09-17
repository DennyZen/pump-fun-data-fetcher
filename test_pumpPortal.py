import asyncio
import websockets
import json

from google_sheets import write_to_google_sheets,  big_last_row
from helpers.utils import get_coin_data
wallet_addresses = ['4ogB5gWF3Vvu4zswi8xpugD8o3Kx2zr7f4fwTTm45oCJ',
 'ErAZT2DJ2P57k5hZEqViz6QH1bp2VyRwLRivUwLtHbyz',
 '7nuD19Drajx9Wb6kbACkNGrzYFQWvXtZCKYMXuXKMfQm',
 'zCwNoMuezdDaRVQyk6xdj7eKmVCEq7TBBmM4zXPnALy',
 'EE32cTEqdA4JnJhdWkszxxcWZ45QgkD2kxhSW5Vk9aje',
 'AGzev4whXDRoAEw2znVZMpjUGf54xhXZK8mHt8jQFNZ6',
 'nSt55VVPLRcfSWrMK1tv3mGzyZNJUd7UXdLtb6BhAPS',
 'B6wjb9ozqGSTbPMyE2nPvRWY19gPhBsxpFtEqtJcUq1o',
 '2au2qqN81edcz97UMWhzribhsrDdVbrM2ohgDQuNaXup',
 'ES9FLeYDoXi29bNKQPYRQCMGfqCRxizUjfdRNyTnmX5T',
 '9Woc9XJG48wtbSwGHusDthPeoZ7cbCWTN8pRu8esqWjQ',
 'JmH3rty1oEqdSDNUZeTZo9hkiyBKC6FiuwpqAYefPhd',
 'AK9M1g73tuAgn62USNTx84ZJ5U28itkf6pK7pMy9VN4j',
 'qDXUuA1QFbREvcTWCqU6tW3tuVUZVCfieWnA315L3eq',
 '2WXMqANBCWQhkPft6YSiYy9XnL3xbkcxmBfhHDrYxJPY',
 'B8kepswMFC6k6HjTe2waYNAufyg5Rtd1KX5srQLjxNpZ',
 'c7Mf9wuparv5G8vrZbrLxh7Mb9CdEsqRgeMWcK7wobb',
 'EkcUBPy95pcwkXxP8z5U4JuP8ydiFfBWYXkLsS22V4o7',
 '84PP1y9kXp15dd2JAVATQeb4sbgt7Vcv7gstrm2EMrEK',
 'HypXUZvd9g7i9qgvTpFNQD541Re4n38AJ5VnjPXu6eUe',
 '2HAvBvM2Rzr9ztrxBnTStkm3c3Ntwgniw8S1UyEumtru',
 '5f4kiYGjpV4TdbMLiENGcGV6AnJTQkoDrvcoLGoLrQRE',
 'Cve9cywd1xdjYGfttwZCQsfhCe9hDZSsXUGw1UNPeMyz',
 'CiboWjN7Sq38EBN9rD4RXQHvury6kdH9osg3kpdWxWef',
 'Aecs9UhSV6R1uxz52RszH3yobXGLu64px4PLMpCBqHU2']
wallet_addresses = [
    "3eJkwFDZVB27emciij1oWUVodmFhFdnkpmzKHjDzH34o",
    "CPUvH6fYkpYBK5raccquTMNJAGc6eQ37VVqBgHq3hwjp",
    "7Gt57NfrPD82K8YpTsSijPB2tfdob7Hy1nU7C67P1J52",
    "4uZbWYcAk3Wuw2cyFXK2Cw7Mo38khTz9phC3VD1KXTbX",
    "BDFMkurHjWM8HCibLRncxaSF8eQ3oJJztPSr4jUEo3nZ",
    "D4zVhwuUsFbcaty7wJhNEZ7VEwPHXQ5d2heXPxM5yWhL",
    "A67uuHBkB4MW6GoFYyiymKGKSDYDwvFPNF5XFqSM8q5L"
]

wallet_addresses+=['4mH6ENXnLCLf98BCz5BVHfUHDvV6c4wKeDLjAoMxu5Ja','F46fkvycu8cRRB7Z2pnkkCug7a2m1crSBGdjPoCsHvNA', 'A719nD9SkNrG2EQP6CLQFURVKcqfqrT6AJSN3MnR6HSB']
# From Ray Wallet tracker
CA = '3Tu6nPNdfvqNobQkMgJDwZe1LBve9sRUDQhssqxWK1hL'  # ORACLE

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
                msg = ""

                # Проход по словарю
                for key, value in payload.items():
                    msg += f" {key} : {value}\n"

                #print(f"payload = {payload=}")
                big_last_row(bold=False, font_size=10)
                #msg = 'subscribed to Wallets: '+', '.join(wallet_addresses)
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
                coin_data=get_coin_data(msg_dict['mint'])
                print(json.dumps(coin_data, indent=4))
                msg = [msg_dict['mint'], msg_dict['txType'], msg_dict['tokenAmount'], msg_dict['newTokenBalance'], msg_dict['marketCapSol'], msg_dict['traderPublicKey'], coin_data.get('symbol','')]
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
# payload = [payload2, payload3]

asyncio.get_event_loop().run_until_complete(subscribe(payload3))