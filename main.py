from flask import Flask, request, jsonify
from runner.controllers import AnswerController
from config import config
import requests
import json
app = Flask(__name__)

@app.route('/')
def answers():
    return AnswerController.AnswerController().index()
@app.route('/respond')
def respond():
    data=json.dumps({
                    "messaging_product": "whatsapp",    
                    "recipient_type": "individual",
                    "to": "254751148166",
                    "type": "text",
                    "text": {
                        "preview_url": False,
                        "body": "Welcome to Whatapp Runner."
                    }
            })
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {config['WhatsappAccessToken']}"}
    response = requests.post(config['WhatsappURL'], data=data,
            headers=headers)

    return json.dumps(response), 200

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == config['MetaCallbackToken']:
                return "Verification token mismatch"
            return jsonify(int(request.args['hub.challenge']))
    elif request.method == 'POST':
        data=json.dumps({
                    "messaging_product": "whatsapp",    
                    "recipient_type": "individual",
                    "to": "254751148166",
                    "type": "text",
                    "text": {
                        "preview_url": False,
                        "body": "Welcome to Whatapp Runner."
                    }
            })
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {config['WhatsappAccessToken']}"}
        requests.post(config['WhatsappURL'], data=data,
            headers=headers)
        return { "message": "Message sent successfully" }, 200

if __name__ == '__main__':
    app.run()