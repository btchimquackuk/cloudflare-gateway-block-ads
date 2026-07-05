import os
import requests

# Load environment variables from GitHub Secrets
API_TOKEN = os.getenv("CLO_API_TOKEN")
ACCOUNT_ID = os.getenv("CLO_ACCOUNT_ID")
# Replace this with your actual Cloudflare Gateway List ID
LIST_ID = "YOUR_CLOUDFLARE_LIST_ID" 

URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/gateway/lists/{LIST_ID}/items"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def sync_list():
    # Read the downloaded text file
    if not os.path.exists("blocklist.txt"):
        print("Error: blocklist.txt not found!")
        return

    with open("blocklist.txt", "r") as f:
        # Filter out empty lines and comments
        domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    # Cloudflare API allows appending or replacing items. 
    # To overwrite the list entirely with fresh data, we send a PUT request
    # Chunking into groups of 1000 items to stay safe within API limits
    for i in range(0, len(domains), 1000):
        chunk = domains[i:i+1000]
        payload = {"append": [{"value": d} for d in chunk]}
        
        response = requests.post(URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            print(f"Successfully synced items {i} to {i+len(chunk)}")
        else:
            print(f"Failed to sync chunk starting at {i}: {response.text}")

if __name__ == "__main__":
    sync_list()
