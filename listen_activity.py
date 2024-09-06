import asyncio
import websockets
import json
import csv

# Функция для чтения списка кошельков из CSV-файла
def read_wallets_from_csv(filename):
    wallets = []
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            wallets.append(row[0])  # Предполагаем, что каждый кошелек находится в новой строке
    return wallets

# Асинхронная функция для отслеживания активности кошельков
async def listen_to_wallet_activity(wallet_addresses):
    async with websockets.connect("wss://api.mainnet-beta.solana.com") as websocket:
        # Подписка на все транзакции для заданных кошельков
        subscription_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "logsSubscribe",
            "params": ["all", {"mentions": wallet_addresses}]
        }
        await websocket.send(json.dumps(subscription_request))
        
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print(f"Received transaction data: {data}")

# Основная программа
if __name__ == "__main__":
    csv_filename = 'wallets.csv'  # Укажите имя вашего CSV-файла
    wallet_addresses = read_wallets_from_csv(csv_filename)
    asyncio.run(listen_to_wallet_activity(wallet_addresses))
