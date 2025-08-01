import requests, base64,datetime, os
from dotenv import load_dotenv

load_dotenv()

def get_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(url, auth=(os.getenv('MPESA_CONSUMER_KEY'), os.getenv('MPESA_CONSUMER_SECRET')))
    return r.json()["access_token"]

def stk_push(phone, amount):
    token = get_token()
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((os.getenv('MPESA_SHORTCODE') + os.getenv('MPESA_PASSKEY') + timestamp).encode()).decode()

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "BussinessShortCode": os.getenv("MPESA_SHORTCODE"),
        "Password": password,
        "Timestamp": timestamp,
        "TranactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": os.getenv("MPESA_SHORTCODE"),
        "PhoneNumber": phone,
        "CallBackURL": os.getenv("MPESA_CALLBACK_URL"),
        "AccountReference": "Test123",
        "TransactionDesc": "Payment Test"
    }

    res = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processreequest",
        headers=headers, json=payload)
    return res.json()