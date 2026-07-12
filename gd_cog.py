from discord.ext import commands, tasks
import discord as dc
from discord import app_commands
import config as cg
import datetime
class GDCog(commands.Cog):
    daily_time = datetime.time(hour=cg.DAILY_QUESTION_TIME[0], minute=cg.DAILY_QUESTION_TIME[1], 
                               second=cg.DAILY_QUESTION_TIME[2], tzinfo=cg.TIMEZONE)
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_member = None
        self.run_daily_question.start()
    
    @commands.command(name="ejemplo")
    async def ejemplo_com(self, ctx):
        await ctx.send("asdasd")
        print("asdasds")

    @app_commands.command(name="galleta", description="Bot te da una galleta 🍪")
    async def dar_galleta(self, interaction: dc.Interaction):
        await interaction.response.send_message("Hola!, toma esta galleta uwu 🍪")
    
    @tasks.loop(time=daily_time)
    async def run_daily_question(self):
        await self.bot.get_channel(self.bot.DAILY_CHANNEL_ID).send("Test de cada 24 horas")
    
    @run_daily_question.before_loop
    async def before_question(self):
        # waiting is ready
        await self.bot.wait_until_ready()
    
    def cog_unload(self):
        self.run_daily_question.cancel() 
    
    # Refreshes all the changable data like timezone and ids
    #@commands.command(name="refresh")
    #async def refresh(self, ctx):
    #    self.daily_time = datetime.time(hour=cg.DAILY_QUESTION_TIME[0], minute=cg.DAILY_QUESTION_TIME[1], 
    #                           second=cg.DAILY_QUESTION_TIME[2], tzinfo=cg.TIMEZONE)
    #    #self.run_daily_question.start()
    #    bot = self.bot
    #    bot.refresh()
    #    self.run_daily_question.restart()
    #    print("Refreshed all time and ids data (to change the guild token you must restart the bot)")

async def setup(bot):
    await bot.add_cog(GDCog(bot))
