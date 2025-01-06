import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from model import Model

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TEXT_MODEL_PATH = os.getenv("TEXT_MODEL_PATH")
URL_MODEL_PATH = os.getenv("URL_MODEL_PATH")

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)
model = Model(TEXT_MODEL_PATH,URL_MODEL_PATH)

async def send_message(message: Message):
    user_message = message.content
    if not user_message:
        print("message was empty (intents may not be enabled)")
        return
    
    try:
        if model.predict(user_message):
            await message.channel.send("Message is considered phishing!!")
    except Exception as e:
        print(e)

@client.event
async def on_ready():
    print(f"{client.user} is running")

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        #prevent the bot from answering itself
        return
    
    user = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f"[{channel}] {user}: {user_message}")
    
    await send_message(message)

def main():
    if TOKEN == None or TEXT_MODEL_PATH == None or URL_MODEL_PATH == None:
        print("Token, text_model_path or url_model_path variable(s) are empty or undefined!")
        exit(1)

    client.run(token=TOKEN)

if __name__ == "__main__":
    main()