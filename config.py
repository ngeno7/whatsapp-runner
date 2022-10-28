from dotenv import load_dotenv
import os

load_dotenv()

config = {
  'AppName': os.environ['AppName'],
  'MetaCallbackToken': os.environ['MetaCallbackToken'],
  'WhatsappAccessToken': os.environ['WhatsappAccessToken'],
  'WhatsappURL': os.environ['WhatsappURL'],
}
