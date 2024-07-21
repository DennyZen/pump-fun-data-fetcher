import helpers.new_tokens
import time
import helpers.get_raydium
import helpers.fifteen_minutes_info
import helpers.one_hour_update
from helpers.fifteen_minutes_info import run_fifteen_minutes_info

from helpers.database import TOKENS
from google_sheets import write_to_google_sheets


def main():
  while True:
    DATA_TO_INSERT = []
    tokens  = [] # TOKENS.find()
    run_fifteen_minutes_info()
    break
    for token in tokens:
      DATA_TO_INSERT.append(
        [
          None,
          token['mcapEveryH'],
          None,
          None,
          token['mcap15min/launch'],
          token['tgSubs15min'],
          token['twitterFollowers'],
          None,
          token['telegramLiveCall'],
          token['telegramMembers'],
          str(token['launchDate']),
          token['updatedAt'],
          token['lunarCrushGalaxyScore'],
          token['lunarCrushAltRank'],
          token['lunarCrushSocialDominance'],
          token['lunarCrushSocialScore'],
          token['highestPercetageOfHolder'],
          token['allTimeHighMcap'],
          token['mcapATH/mcap15min'],
          token['Name'],
          f"https://dexscreener.com/solana/{token['contractAddress']}",
          token['launchMcap'],
          token['mcap15min'],
          token['liquidity15min'],
          token['liquidity15min/mcap15min'],
          token['holders'],
          token['5minVolume15min'],
          "1" if token['image'] else "0",
          "1" if token['twitter'] else "0",
          "1" if token['telegram'] else "0",
          "1" if token['website'] else "0",
          token['percentOfTop5Holders'].replace(" ", "") if token['percentOfTop5Holders'] else None,
        ]
      )
    #write_to_google_sheets(DATA_TO_INSERT)
    print("Script is running!")
    #time.sleep(15)

def get_token_info(token_name):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
    parameters = {
        'symbol': token_name
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    
    if 'data' in data and token_name.upper() in data['data']:
        return data['data'][token_name.upper()]
    else:
        return None
    

def get_token_info_by_id(token_id):
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
    parameters = {
        'id': token_id
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    
    if 'data' in data and str(token_id) in data['data']:
        return data['data'][str(token_id)]
    else:
        return None
def get_token_all_time_high(token_symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': token_symbol,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    print(data)
    if 'data' in data and token_symbol.upper() in data['data']:
        all_time_high = data['data'][token_symbol.upper()]['quote']['USD']['all_time_high']
        print(json.dumps(data['data'][token_symbol.upper()], indent=4))
        return all_time_high
    return None
if __name__ == "__main__":
  key = '50aaf0c6-9e74-4753-bf7b-6d4f5e98344e'
  key2 = '791db534-aa9c-4483-9a1a-8d15cee093a9'
  import requests
  import json

  # Вставьте ваш API ключ CoinMarketCap
  api_key = '791db534-aa9c-4483-9a1a-8d15cee093a9'


  token_id = 31967  # Уникальный ID токена (например, для Solana)
  token_info = get_token_info_by_id(token_id)
  token_name = 'WATER'  # Название токена
  #token_info = get_token_info(token_name)
  #allTimeHighMcap = get_token_all_time_high(token_name)
  #print(f"All time high Mcap of {token_name}: {allTimeHighMcap:,}")

  if token_info:
      print(json.dumps(token_info, indent=4))
      supply = token_info['self_reported_circulating_supply']
      market_cap = token_info['self_reported_market_cap']
      print(f"Market cap: {market_cap:,}")
      print(f"Circulating supply: {supply:,}")  

  else:
      print("Token not found or error in request.")

  main()