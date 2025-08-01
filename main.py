from flask import Flask, request, jsonify
from stk_push import stk_push
from sms_sender import send_sms, send_bulk_sms

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
    data = request.get_json()
    result = data['Body']['stkCallback']['ResultDesc']
    phone = mpesa_data['Body']['stkCallback']['CallbackMetadata']['Item']['4']['value']
    
    #send sms with payment result\\
    send_bulk_sms([phone], f"Your sub {result}")
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

if __name__ == "__main__":
    app.run(port=5000)
