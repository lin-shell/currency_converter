import requests

url = "http://127.0.0.1:5000/overwrite_rate"
# payload = {"ccy_from": "EUR", "ccy_to": "GBP", "quantity": 1000}
headers = {"Content-Type": "application/json"}


payload = {
    "overwrites": [
        {
            "ccy_from": "USD",
            "ccy_to": "GBP",
            "rate": 0.7
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
response.raise_for_status()
print(response.json())
