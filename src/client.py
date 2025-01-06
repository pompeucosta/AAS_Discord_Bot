from discord import Client, Message
from model import Model

class BotClient(Client):
    def __init__(self,intents,model: Model):
        super().__init__(intents=intents)
        self.model = model

    async def on_ready(self):
        print(f"{self.user} is running")

    async def on_message(self,message: Message):
        if message.author == self.user:
            #prevent the bot from answering itself
            return
        
        user = str(message.author)
        user_message = message.content
        channel = str(message.channel)

        print(f"[{channel}] {user}: {user_message}")
        
        await self._send_message(message)

    async def _send_message(self,message: Message):
        user_message = message.content
        if not user_message:
            print("message was empty (intents may not be enabled)")
            return
        
        try:
            if self.model.predict(user_message):
                await message.reply("This message is considered phishing!!",mention_author=True)
        except Exception as e:
            print(e)
        