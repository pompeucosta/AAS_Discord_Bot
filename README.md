# Phishing detection discord bot
Discord bot developed to warn server users if a message is considered a phishing message.

This bot was developed within the scope of a university project, with the main goal being the development of a machine learning model capable of identifying phishing messages.
It's not meant for real world scenarios as it is a simple model and script.

## Creating the bot
To create a bot, the first step is to go to the [applications page in the discord developer portal](https://discord.com/developers/applications).
Once there, click on the ``New Application`` button (or use an already created application).

After the application is created, go to the ``Bot`` settings.
In that page, enable ``Message Content Intent`` just above the ``Bot Permissions`` section and click on the ``Reset Token`` button.
This will create a token that will only be shown once.
Copy the token generated and create a file ``.env`` in the ``src`` folder (if it doesn`t already exist).
Create a variable ``DISCORD_TOKEN`` and set the token as its value, for example:

```
DISCORD_TOKEN=<token_generated>
```

Now, go to the ``OAuth2`` settings and in the ``OAuth2 URL Generator`` section enable the ``bot`` checkbox.
To add the bot to a server, copy the url generated and paste it in a new browser tab.
Follow the prompts and the bot will be fully setup.

## Before running the bot
The default behaviour of the bot requires some environmental variables to be set:
| Env variable | Description |
|-------------------|-------------|
| `TEXT_MODEL_PATH` | The path to the model that predicts text messages |
| `URL_MODEL_PATH` | The path to the model that predicts URLs |
| `TLD_ENCODER_PATH` | The path to the encoder that encodes the TLDs in feature extraction |

> [!NOTE]
> It's possible to use your own models.
> For that simply create a class to represent your model and implement the `predict` method:
> ```python
> class MyModel(Model):
>     def predict(self,message: str,urls: list[str]):
>         # your model predict behaviour
> ```
> The main script will automatically load the environmental variables, so you can just retrieve them on your class.
> Then, in main, just create an instance of your model class and pass it to the `ModelHandler`.


## Running the bot
To run the bot, all that is needed is to install the requirements and run the main python script

```bash
python src/main.py
```

The bot will be ready once it prints the following:
```
INFO     discord.client logging in using static token
INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: 5d9ec7294cf42393fca42476774bf992).
<bot name>#<bot number> is running
```
