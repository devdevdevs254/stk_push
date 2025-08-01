import africastalking, os
from dotenv import load_dotenv
load_dotenv()

africastalking.initialize(os.getenv("AT_USERNAME"), os.getenv("AT_API_KEY"))
sms = africastalking.SMS

def send_sms(phone, mesage):
    try:
        response = sms.send(message, [phone])
        return response
    except Exception as e:
        return str(e)