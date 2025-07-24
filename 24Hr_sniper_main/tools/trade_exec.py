import requests

RECALL_API_URL = "https://api.competitions.recall.network/sandbox/api/trade/execute"
API_KEY = "your_api_key_here"  # Replace with your actual Recall API key. Get one here: https://register.recall.network/

def recall_trade_tool(fromToken: str, toToken: str, amount: str, reason: str) -> dict:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    trade_data = {
        "fromToken": fromToken,
        "toToken": toToken,
        "amount": amount,
        "reason": reason
    }

    response = requests.post(RECALL_API_URL, json=trade_data, headers=headers)
    try:
        return response.json()
    except Exception as e:
        return {"error": str(e)}

