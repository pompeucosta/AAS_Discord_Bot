# Discord bot
Discord bot developed to warn server users if a message is considered a phishing message.

This bot was developed with the scope of the AAS project, with the main goal being the development of a machine learning model capable of identifying phishing messages.
It's not meant for real world scenarios as it is a simple model and script.

## Creating the bot
To create a bot, the first step is to go to the [applications page in the discord developer portal](https://discord.com/developers/applications).
Once there, click on the ``New Application`` button (or use an already created application).

After the application is created, go to the ``Bot`` settings and click on the ``Reset Token`` button.
This will create a token that will only be shown once.
Copy the token generated and create a file ``.env`` in the ``src`` folder.
Create a variable ``DISCORD_TOKEN`` and set the token as its value, for example:

```
DISCORD_TOKEN=<token_generated>
```

Now, go to the ``OAuth2`` settings and in the ``OAuth2 URL Generator`` section enable the ``bot`` checkbox.
To add the bot to a server, copy the url generated and paste it in a new browser tab.
Follow the prompts and the bot will be fully setup.

## Running the bot
To run the bot, all that is needed is to install the requirements and run the main python script

```bash
python3 src/main.py
```