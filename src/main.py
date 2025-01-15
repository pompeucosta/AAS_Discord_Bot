from os import getenv
from dotenv import load_dotenv
from discord import Intents
from modelHandler import ModelHandler
from model import MyTrainedModel, PhisingURLModel
from client import BotClient

def main():
    load_dotenv()
    TOKEN = getenv("DISCORD_TOKEN")
    
    if TOKEN == None:
        print("Token undefined!")
        exit(1)

    # model to predict text messages
    text_model = MyTrainedModel()

    # model to predict urls
    url_model = PhisingURLModel()

    intents = Intents.default()
    intents.message_content = True
    model = ModelHandler(text_model,url_model)
    client = BotClient(intents,model)

    client.run(token=TOKEN)

if __name__ == "__main__":
    main()