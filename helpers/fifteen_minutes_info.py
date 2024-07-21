from helpers.database import TOKENS
from datetime import datetime
import requests
from helpers.utils import get_solana_top_token_holders, get_token_holder_count
from helpers.utils import format_numbers
import time
import threading
import certifi
import pprint


def get_fifteen_minutes_info():
    #tokens = TOKENS.find({"state": "early"})
    tok={}
    tokens = [tok]
    for token in tokens:
        #token_launch_date = token["launchDate"]
        token['contractAddress'] = "B6h248NJkAcBAkaCnji889a26tCiGXGN8cxhEJ4dX391"

        # Check if token has been launched for 15 minutes
        current_time = datetime.now()
        time_difference = 1000 #current_time - token_launch_date

        if True: #time_difference.total_seconds() >= 900:
            response = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{token['contractAddress']}", verify=certifi.where())
            data = response.json()
            print('From DEXScreen:')
            
            more_info = data["pairs"][0]
            pprint.pprint(format_numbers(more_info))
            try:
              holders = get_token_holder_count(token['contractAddress'])
            except Exception as e:
              print("Error getting holders")
              import traceback
              print(traceback.format_exc())
              
              holders = None
            try:   
              token['totalSupply'] = 73111061995
              token['launchMcap'] = 1000
              token['allTimeHighMcap'] = 40000000
              top_holder, top_five_holders = get_solana_top_token_holders(token['contractAddress'], token['totalSupply'])
            except Exception as e:
              print("Error getting top holders")
              import traceback
              print(traceback.format_exc())

              print(f"An error occurred while getting top holders: {str(e)}")
              top_holder = None
              top_five_holders = None
            print(top_five_holders)
            result0 =  {
                        "mcap15min/launch": more_info['fdv'] / token['launchMcap'],
                        "mcap15min": more_info["fdv"],
                        "mcapATH/mcap15min": token['allTimeHighMcap'] / more_info['fdv'],
                        "liquidity15min": more_info["liquidity"]['usd'],
                        "liquidity15min/mcap15min": more_info["liquidity"]['usd'] / more_info["fdv"],
                        "5minVolume15min": more_info["volume"]['m5'],
                        "state": "fifteen_minutes",
                        "allTimeHighMcap": more_info['fdv'] if more_info['fdv'] > token['allTimeHighMcap'] else token['allTimeHighMcap'],
                        "holders": holders,
                        "percentOfTop5Holders": " ".join(top_five_holders) if top_five_holders else None,
                        "highestPercetageOfHolder": top_holder,
                        "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
            
            res = format_numbers(result0)
            pprint.pprint(res)
            # TOKENS.update_one(
            #     {"contractAddress": token["contractAddress"]},
            #     {
            #         "$set": {
            #             "mcap15min/launch": more_info['fdv'] / token['launchMcap'],
            #             "mcap15min": more_info["fdv"],
            #             "mcapATH/mcap15min": token['allTimeHighMcap'] / more_info['fdv'],
            #             "liquidity15min": more_info["liquidity"]['usd'],
            #             "liquidity15min/mcap15min": more_info["liquidity"]['usd'] / more_info["fdv"],
            #             "5minVolume15min": more_info["volume"]['m5'],
            #             "state": "fifteen_minutes",
            #             "allTimeHighMcap": more_info['fdv'] if more_info['fdv'] > token['allTimeHighMcap'] else token['allTimeHighMcap'],
            #             "holders": holders,
            #             "percentOfTop5Holders": " ".join(top_five_holders) if top_five_holders else None,
            #             "highestPercetageOfHolder": top_holder,
            #             "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            #         }
            #     },
            #)


def run_fifteen_minutes_info():
    get_fifteen_minutes_info()
    # while True:
    #     get_fifteen_minutes_info()
    #     time.sleep(10)


#fifteen_minutes_thread = threading.Thread(target=run_fifteen_minutes_info, daemon=True)
#fifteen_minutes_thread.start()
