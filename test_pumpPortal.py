import asyncio
import websockets
import json

from google_sheets import write_to_google_sheets

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
CA = '5FMjMuiAdgwF3REQogMqrdLRBF9pKs5wfJ9hW71Fpump'

async def subscribe(payload):
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(payload))
        
        async for message in websocket:
            dict = json.loads(message)
            print(dict)
            if 'name' in dict:
                print(f'message1 {dict["name"]} {dict["marketCapSol"]} ')
                write_to_google_sheets([[dict["marketCapSol"],dict["name"]]])

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

asyncio.get_event_loop().run_until_complete(subscribe(payload3))