import discord as dc
from dotenv import load_dotenv
import os
from gd_bot import GDQuiz

if __name__ == "__main__":

    load_dotenv("credentials.env")
    TOKEN = os.getenv("TOKEN")
    intents = dc.Intents.default()
    intents.message_content = True

    client = GDQuiz(intents=intents, command_prefix='$')

    client.run(TOKEN)
