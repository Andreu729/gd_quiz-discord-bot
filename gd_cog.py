from discord.ext import commands

class GDCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_member = None
    
    @commands.command(name="ejemplo")
    async def ejemplo_com(self, ctx):
        await ctx.send("asdasd")
        print("asdasds")

async def setup(bot):
    await bot.add_cog(GDCog(bot))
