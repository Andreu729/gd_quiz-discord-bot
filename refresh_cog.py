from discord.ext import commands
import discord as dc
import config as cg
import importlib
from dotenv import load_dotenv
import os
from discord import app_commands

class RefreshCog(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="refresh", description="[🔧 DEV COMMAND]: Use it for refreshing config and .env data without restarting the whole bot")
    async def refreshes(self, interaction: dc.Interaction):
        await interaction.response.send_message("Hola!, toma esta galleta uwu 🍪")
        load_dotenv("credentials.env", override=True)
        bot = self.bot
        try:
            bot.DAILY_CHANNEL_ID = os.getenv("DAILY_CHANNEL_ID")
            bot.DAILY_CHANNEL_ID = int(bot.DAILY_CHANNEL_ID)
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

async def setup(bot):
    await bot.add_cog(RefreshCog(bot))