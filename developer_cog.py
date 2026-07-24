from discord.ext import commands
import discord as dc
import config as cg
import importlib
from dotenv import load_dotenv
import os
from discord import app_commands
from gd_data import (QuestionGD, insert_question, obtain_questions, 
                     modify_question, delete_question, obtain_single_question)
from gd_ui import question_embed, QuestionButtonsView
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
        difficulty="Set a difficulty level from: (Muy Fácil, Fácil, Intermedia, Difícil, Imposible)",
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
    
    @app_commands.command(name="obtain_questions", description="[🔧 DEV COMMAND]: Use it to print all available questions in the bot console")
    @app_commands.check(dev_allowed_channel)
    @app_commands.default_permissions(administrator=True)
    async def obtain_questions_command(self, interaction: dc.Interaction):
        questions = await obtain_questions(cg.OBTAIN_QUESTIONS_LIMIT)
        await interaction.response.send_message(questions[:10])

    @app_commands.command(name="modify_question", description="[🔧 DEV COMMAND]: Use it to modify one parameter of one question by id")
    @app_commands.check(dev_allowed_channel)
    @app_commands.choices(parameter=[
    app_commands.Choice(name="difficulty", value="difficulty"),
    app_commands.Choice(name="description", value="description"),
    app_commands.Choice(name="alternatives", value="alternatives"),
    app_commands.Choice(name="ext_alternatives", value="ext_alternatives"),
    app_commands.Choice(name="correct", value="correct")
])
    @app_commands.describe(id="the id of the question to modify", 
                           parameter="the parameter to change", 
                           value="the value of the given parameter")
    @app_commands.default_permissions(administrator=True)
    async def modify_question_command(self, interaction: dc.Interaction, 
                                      id: int, parameter: app_commands.Choice[str], value: str):
        result = await modify_question(id, parameter.name, value)
        if result is True:
            await interaction.response.send_message("Parametro cambiado correctmente")

    @app_commands.command(name="delete_question", description="[🔧 DEV COMMAND]: Use it to delete the question with its id")
    @app_commands.check(dev_allowed_channel)
    @app_commands.describe(id="Id of question to delete")
    @app_commands.default_permissions(administrator=True)
    async def delete_question_command(self, interaction: dc.Interaction, id: int):
        await delete_question(id)
        await interaction.response.send_message(f"Pregunta ID={id} se ha eliminado")

    @app_commands.command(name="print_question", description="[🔧 DEV COMMAND]: Prints the question with that id in the cool format")
    @app_commands.check(dev_allowed_channel)
    @app_commands.describe(id="Id of question to print")
    @app_commands.default_permissions(administrator=True)
    async def print_single_question(self, interaction: dc.Interaction, id: int):
        question = await obtain_single_question(id)
        embed = question_embed(question)
        view = QuestionButtonsView(question=question)
        print(f"print_question: pregunta con id={id} mostrada")
        await interaction.response.send_message(f"Pregunta con id={id} printeada en el chat", ephemeral=True)
        await interaction.channel.send(embed=embed, view=view)
async def setup(bot):
    await bot.add_cog(DeveloperCog(bot))
