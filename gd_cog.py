from discord.ext import commands, tasks
import discord as dc
from discord import app_commands
import config as cg
import datetime
from gd_ui import question_embed, QuestionButtonsView, user_embed
from gd_data import QuestionGD, obtain_user, get_daily_question, User, obtain_user_xp, color_id_to_color
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

    @app_commands.command(name="xp", description="Entrega tu xp acumulada en este Bot")
    async def give_xp(self, interaction: dc.Interaction):
        user_id = interaction.user.id
        xp = await obtain_user_xp(user_id)
        await interaction.response.send_message(f"Tu cantidad de xp total es: {xp}")

    @app_commands.command(name="level", description="Entrega información de tu nivel y tu usuario")
    async def show_user(self, interaction: dc.Interaction):
        user = interaction.user
        user_db = await obtain_user(user.id)
        xp = user_db["xp"]
        level = user_db["level"]
        xp_level = xp - cg.XP_FUNCTION(level)
        color_id = user_db["color"]
        color = color_id_to_color(color_id)
        user_class = User(user, level, total_xp=xp, lvl_xp=xp_level, color=color)
        embed = user_embed(user_class)
        await interaction.response.send_message(embed=embed)

    @tasks.loop(time=daily_time)
    async def run_daily_question(self):
        question = await get_daily_question()
        embed = question_embed(question)
        view = QuestionButtonsView(question=question)
        await self.bot.get_channel(self.bot.DAILY_CHANNEL_ID).send(embed=embed, view=view)
    
    @run_daily_question.before_loop
    async def before_question(self):
        # waiting is ready
        await self.bot.wait_until_ready()
    
    def cog_unload(self):
        self.run_daily_question.cancel() 

async def setup(bot):
    await bot.add_cog(GDCog(bot))
