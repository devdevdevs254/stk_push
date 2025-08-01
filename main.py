from flask import Flask, request, jsonify
from stk_push import stk_push
from sms_sender import send_sms

app = Flask(__name__)

@app.route("/pay", methods=["POST"])
def pay():
    data = request.get_json()
    phone = data["phone"]
    amount = data["amount"]

    result = stk_push(phone, amount)
    return jsonify(result)

@app.route("/callback", methods=["POST"])
def callback():
    mpesa_data = request.get_json()
    phone = mpesa_data['Body']['stkCallback']['CallbackMetadata']['Item']['4']['value']
    status = mpesa_data['Body']['stkCallback']['ResultDesc']

    #send sms with payment result\\
    send_sms(phone, f"Your Payment Status: {status}")
    return jsonify({"ResultCode":0, "ResultDesc":"Accepted"})

if __name__ == "__main__":
    app.run(port=5000)