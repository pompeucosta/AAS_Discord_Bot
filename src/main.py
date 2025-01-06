import os
from dotenv import load_dotenv
from discord import Intents, Client, Message

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
print(TOKEN)