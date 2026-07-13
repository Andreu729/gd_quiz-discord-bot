from discord.ext import commands
import discord as dc
import config as cg
import importlib
from dotenv import load_dotenv
import os
from discord import app_commands
from gd_data import QuestionGD, insert_question

class DeveloperCog(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # podría fallar por el self
    load_dotenv("credentials.env")
    try:
        ALLOWED_DEV_CHANNELS = os.getenv("ALLOWED_DEV_CHANNELS")
        ALLOWED_DEV_CHANNELS = ALLOWED_DEV_CHANNELS.split(",")
        ALLOWED_DEV_CHANNELS = [int(channel) for channel in ALLOWED_DEV_CHANNELS]
    except ValueError:
        print(f"[ERROR]: DAILY_CHANNEL_ID must have elements convertible to int!")
    @staticmethod
    def dev_allowed_channel(interaction: dc.Interaction, ALLOWED_DEV_CHANNELS=ALLOWED_DEV_CHANNELS) -> bool:
        # Returns True if it's allowed, False otherwise
        return interaction.channel_id in ALLOWED_DEV_CHANNELS

    @app_commands.command(name="refresh", description="[🔧 DEV COMMAND]: Use it for refreshing config and .env data without restarting the whole bot")
    @app_commands.default_permissions(administrator=True)
    async def refreshes(self, interaction: dc.Interaction):
        await interaction.response.send_message("Hola!, toma esta galleta uwu 🍪")
        load_dotenv("credentials.env", override=True)
        bot = self.bot
        try:
            bot.DAILY_CHANNEL_ID = os.getenv("DAILY_CHANNEL_ID")
            bot.DAILY_CHANNEL_ID = int(bot.DAILY_CHANNEL_ID)
            ALLOWED_DEV_CHANNELS = os.getenv("ALLOWED_DEV_CHANNELS")
            ALLOWED_DEV_CHANNELS = ALLOWED_DEV_CHANNELS.split(",")
            self.ALLOWED_DEV_CHANNELS = [int(channel) for channel in ALLOWED_DEV_CHANNELS]
        except ValueError:
            print(f"[ERROR]: DAILY_CHANNEL_ID must be convertible to an int!: int(DAILY_CHANNEL_ID) fails")
        try:
            bot.GUILD_ID = os.getenv("GUILD_ID")
            bot.GUILD_ID = int(bot.GUILD_ID)
        except ValueError:
            print(f"[ERROR]: GUILD_ID must be convertible to an int!: int(GUILD_ID) fails")
        importlib.reload(cg)
        await bot.reload_extension("gd_cog")
        print("Refreshed all time and ids data")
    
    @app_commands.command(name="insert_question", description="[🔧 DEV COMMAND]: Use it to insert a new question into the trivia!")
    @app_commands.check(dev_allowed_channel)
    @app_commands.describe(
        difficulty="Set a difficulty level from: (Muy fácil, Fácil, Intermedia, Difícil, Imposible)",
        description="The text of the question",
        alternatives="The alternatives that the question have (must be csv, separated by commas)",
        correct="the index of the correct alternative",
        ext_alternatives="extra alternatives for the point_card (must be csv, separated by commas)"
    )
    @app_commands.default_permissions(administrator=True)
    async def insert_question_command(self, interaction: dc.Interaction, description: str, 
                              difficulty: str, alternatives: str, correct: int, ext_alternatives: str):

        alternatives = alternatives.split(",")
        alternatives = [al.strip() for al in alternatives]
        ext_alternatives = ext_alternatives.split(",")
        ext_alternatives = [al.strip() for al in ext_alternatives]
        question = QuestionGD(desc=description, difficulty=difficulty, alternatives=alternatives,
                              correct=correct, ext_alternatives=ext_alternatives)
        await insert_question(question)
        print(f"Nueva pregunta añadida: {description}")
        await interaction.response.send_message("pregunta añadida correctamente!")
    # checks if the command where is sent is in the correct channel.

# Comandos faltantes:
# obtain_questions (para obtener las ids y los enunciados
# modify_question (para modificar un elemento de la base según id)
# remove_question (para eliminar un elemento según id)
async def setup(bot):
    await bot.add_cog(DeveloperCog(bot))
