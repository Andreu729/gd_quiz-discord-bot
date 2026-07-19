from discord.ext import commands, tasks
import discord as dc
from discord import app_commands
import config as cg
import datetime
from gd_ui import QuestionExample, question_embed, QuestionButtonsView
from gd_data import QuestionGD
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
    
    #@tasks.Loop(time=daily_time)
    @tasks.loop(seconds=60.0)
    async def run_daily_question(self):
        view = QuestionExample()
        #desc = "Quién es el creador del famoso nivel **Nine Circles**?"
        desc = "Oficialmente, cuál de estos triggers **no existe** en el editor?"
        diff = "Fácil"
        question = QuestionGD(desc=desc, difficulty=diff, alternatives=["Spawn Trigger", "Touch Trigger", "On Restart Trigger", "Random Trigger"], correct=2, ext_alternatives=["On Death Trigger", "Advanced Follow Trigger"])
        view = QuestionButtonsView(question=question)
        embed = question_embed(desc, diff)
        await self.bot.get_channel(self.bot.DAILY_CHANNEL_ID).send(embed=embed, view=view)
    
    @run_daily_question.before_loop
    async def before_question(self):
        # waiting is ready
        await self.bot.wait_until_ready()
    
    def cog_unload(self):
        self.run_daily_question.cancel() 

async def setup(bot):
    await bot.add_cog(GDCog(bot))
