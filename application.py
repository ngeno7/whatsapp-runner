from flask import Flask, request, jsonify
from runner.controllers import AnswerController
from config import config
import requests
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

application = Flask(__name__)

@application.route('/')
def answers():
    return AnswerController.AnswerController().index()
@application.route('/respond')
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
    requests.post(config['WhatsappURL'], data=data,
            headers=headers)

    return "Message sent", 200

@application.route('/callback', methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == config['MetaCallbackToken']:
                return "Verification token mismatch"
            return jsonify(int(request.args['hub.challenge']))
    elif request.method == 'POST':
        if len(request.json['entry'][0]['changes']) and 'statuses' in request.json['entry'][0]['changes'][0]['value']:
            print('checking statuses')
        if len(request.json['entry'][0]['changes']) and 'messages' in request.json['entry'][0]['changes'][0]['value']:
            bot = ChatBot(
                'WhatsappRunner',
                # storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri=None,
                read_only=True,
                logic_adapters=[
                    'chatterbot.logic.BestMatch'
            ])

            corpus_trainer = ChatterBotCorpusTrainer(bot)
            # corpus_trainer.train('chatterbot.corpus.english')
            corpus_trainer.train('training_data.linux')
            response = str(bot.get_response(str(request.json['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']).lower()))
            data=json.dumps({
                        "messaging_product": "whatsapp",    
                        "recipient_type": "individual",
                        "to": "254751148166",
                        "type": "text",
                        "text": {
                            "preview_url": False,
                            "body": f"{response}"
                        }
                })
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {config['WhatsappAccessToken']}"}
            requests.post(config['WhatsappURL'], data=data,
               headers=headers)
            return { "message": "Message sent successfully" }, 200
        return { "message": "Lorem ipsum" }, 200

@application.route('/chatbot', methods=['GET'])
def chatbot():
    bot = ChatBot(
    'WhatsappRunner',
    # storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri=None,
    read_only=True,
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ])

    corpus_trainer = ChatterBotCorpusTrainer(bot)
    # corpus_trainer.train('chatterbot.corpus.english')
    corpus_trainer.train('training_data.linux')
    response = str(bot.get_response(str('cp').lower()))

    return response, 200

if __name__ == '__main__':
    application.run()
