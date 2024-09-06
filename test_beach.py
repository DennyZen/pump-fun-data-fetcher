import requests , json

# API Key stored inside the functions
API_KEY = "a507c1eb-5e82-4591-937e-8ba27ffbf482"

def send_api_request(url, method="GET", params=None, data=None):
    """
    Sends an API request and returns the response.

    Args:
        url (str): The API endpoint URL.
        method (str): HTTP method to use (GET, POST, etc.). Default is "GET".
        params (dict): URL parameters to send with the request. Default is None.
        data (dict): Data to include in the body of the request (for POST, PUT, etc.). Default is None.

    Returns:
        dict: The parsed JSON response from the API, or an error message if the request fails.
    """
    headers = {
        'Authorization': API_KEY
    }

    try:
        # Make the API request
        response = requests.request(method, url, headers=headers, params=params, data=data)

        # Check if the response was successful
        if response.status_code == 200:
            return response.json()
        else:
            return {
                'error': f"Request failed with status code {response.status_code}",
                'details': response.text
            }
    except Exception as e:
        return {'error': str(e)}

def fetch_account_fields(pubkey):
    """
    Fetches account fields for a specific public key from the Solana Beach API.

    Args:
        pubkey (str): The public key of the account.

    Returns:
        dict: The account fields from the Solana Beach API, or an error message.
    """
    url = f"https://api.solanabeach.io/v1/account/{pubkey}"
    
    # Use the universal send_api_request function
    return send_api_request(url)

def fetch_account_transactions(pubkey, before=None, limit=None):
    """
    Fetches transactions for a specific public key from the Solana Beach API.

    Args:
        pubkey (str): The public key of the account.
        before (str): The signature of the last transaction you want to search backwards from.
        limit (int): The upper limit of transactions to retrieve.

    Returns:
        dict: The transactions from the Solana Beach API, or an error message.
    """
    url = f"https://api.solanabeach.io/v1/account/{pubkey}/transactions"
    
    # Set query parameters
    params = {}
    if before:
        params['before'] = before
    if limit:
        params['limit'] = limit

    # Use the universal send_api_request function
    return send_api_request(url, params=params)

# Example usage for fetching account fields
pubkey = "2JMC8J5ypBULTpPQ9i7G4tbXrAEQGvRn7UJ4CNkJ6rLF"
account_info = fetch_account_fields(pubkey)
print(account_info)

# Example usage for fetching account transactions
before = None# "some_signature"
transactions = fetch_account_transactions(pubkey, before=before, limit=1)
pretty_json = json.dumps(transactions, indent=4) # json.loads(
print(pretty_json)
