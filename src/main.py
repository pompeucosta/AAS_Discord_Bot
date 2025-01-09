from os import getenv
from dotenv import load_dotenv
from discord import Intents
from modelHandler import ModelHandler
from model import MyTrainedModel
from client import BotClient

def main():
    load_dotenv()

    TOKEN = getenv("DISCORD_TOKEN")
    TEXT_MODEL_PATH = getenv("TEXT_MODEL_PATH")
    URL_MODEL_PATH = getenv("URL_MODEL_PATH")
    
    if TOKEN == None or TEXT_MODEL_PATH == None or URL_MODEL_PATH == None:
        print("Token, text_model_path or url_model_path variable(s) are empty or undefined!")
        exit(1)

    # model to predict text messages
    text_model = MyTrainedModel(TEXT_MODEL_PATH)

    # model to predict urls
    # text_model = MyCustomURLModel(URL_MODEL_PATH)

    intents = Intents.default()
    intents.message_content = True
    # TODO: mudar None pelo modelo dos urls
    model = ModelHandler(text_model,None)
    client = BotClient(intents,model)

    client.run(token=TOKEN)

if __name__ == "__main__":
    main()