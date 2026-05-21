from flask import Flask, request
import requests
import base64
from datetime import datetime

app = Flask(__name__)

# TELEGRAM BOT TOKEN
BOT_TOKEN = "8495768390:AAFX_3qXdPEAa-86plvC3sZoEsVzxycxIQ0"

# MPESA DETAILS
consumer_key = "JKHIGS0ZAVquEJprDXOfujcUQRT50JUCm0xiF5XJUAx0GZwi"
consumer_secret = "xi6PgJG19TJJb1zF5aHlI8l0Aj3NyQ30mQrrmsNs5EcAmr3TVzX28OelMnnKAPq3"

shortcode = "174379"

passkey = "bfb279f9aa9bdbcf158e97dd9fe2815da4f4f1b6c0c0f1b0c6b4f8b3f5f5e"


@app.route('/')
def home():
    return "M-Pesa Telegram Bot Running"


@app.route('/pay', methods=['POST'])
def pay():

    data = request.json

    phone = data['phone']
    amount = data['amount']

    # GENERATE ACCESS TOKEN
    auth = base64.b64encode(
        f"{consumer_key}:{consumer_secret}".encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {auth}"
    }

    response = requests.get(
        "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
        headers=headers
    )

    access_token = response.json()['access_token']

    # TIMESTAMP
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # PASSWORD
    password = base64.b64encode(
        f"{shortcode}{passkey}{timestamp}".encode()
    ).decode()

    stk_headers = {
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": "https://example.com/callback",
