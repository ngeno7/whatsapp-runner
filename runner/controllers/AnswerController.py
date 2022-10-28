import json
class AnswerController:
    def index(self):
        return json.dumps(
          [
            {
                'name': 'Hello'
            },
            {
                'name': 'World'
            }
        ],
        )