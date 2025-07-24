import os
import requests
from dotenv import load_dotenv
 
load_dotenv()                                      # read .env
 
API_KEY  = os.getenv("RECALL_API_KEY")             # never hard‑code
BASE_URL = "https://api.competitions.recall.network"
 
# ---- CONFIG ------------------------------------------------------------------
ENDPOINT = f"{BASE_URL}/api/trade/execute"  # use /api/... for production
FROM_TOKEN = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"   # USDC
TO_TOKEN   = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"   # WETH
AMOUNT_USDC = "50"  # human units; the backend handles decimals
# ------------------------------------------------------------------------------
 
payload = {
    "fromToken": FROM_TOKEN,
    "toToken":   TO_TOKEN,
    "amount":    AMOUNT_USDC,
    "reason":    "Eth trade"
}
 
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type":  "application/json"
}
 
print("⏳  Submitting trade to Recall …")
resp = requests.post(ENDPOINT, json=payload, headers=headers, timeout=30)
 
if resp.ok:
    print("✅  Trade executed:", resp.json())
else:
    print("❌  Error", resp.status_code, resp.text)
