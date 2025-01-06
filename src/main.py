from os import getenv
from dotenv import load_dotenv
from discord import Intents
from model import Model
from client import BotClient

load_dotenv()

TOKEN = getenv("DISCORD_TOKEN")
TEXT_MODEL_PATH = getenv("TEXT_MODEL_PATH")
URL_MODEL_PATH = getenv("URL_MODEL_PATH")

intents = Intents.default()
intents.message_content = True
model = Model(TEXT_MODEL_PATH,URL_MODEL_PATH)
client = BotClient(intents,model)

def main():
    if TOKEN == None or TEXT_MODEL_PATH == None or URL_MODEL_PATH == None:
        print("Token, text_model_path or url_model_path variable(s) are empty or undefined!")
        exit(1)

    client.run(token=TOKEN)

if __name__ == "__main__":
    main()