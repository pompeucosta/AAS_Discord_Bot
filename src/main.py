import os
from dotenv import load_dotenv
from discord import Intents, Client, Message

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

def get_response(user_message: str):
    return "response"

async def send_message(message: Message):
    user_message = message.content
    if not user_message:
        print("message was empty (intents may not be enabled)")
        return
    
    try:
        response = get_response(user_message)
        await message.channel.send(response)
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
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()