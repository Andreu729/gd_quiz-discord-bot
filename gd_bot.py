import discord as dc
from discord.ext import commands
from dotenv import load_dotenv
import os
import time

class GDQuiz(commands.Bot):
    load_dotenv("credentials.env")
    GUILD_ID = None
    try:
        DAILY_CHANNEL_ID = os.getenv("DAILY_CHANNEL_ID")
        DAILY_CHANNEL_ID = int(DAILY_CHANNEL_ID)
    except ValueError:
        print(f"[ERROR]: DAILY_CHANNEL_ID must be convertible to a int!: int(DAILY_CHANNEL_ID) fails")
    try:
        GUILD_ID = os.getenv("GUILD_ID")
        GUILD_ID = int(GUILD_ID)
    except ValueError:
        print(f"[ERROR]: GUILD_ID must be convertible to a int!: int(GUILD_ID) fails")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.time_begin = time.monotonic()
        self.timer_pepe = 0
        self.guild = None
    
    async def on_ready(self):
        print("Cliente iniciado lol xd")
        self.guild = dc.utils.get(self.guilds, id=self.GUILD_ID)
            
        print(f"{self.user} conectado en {self.guild.name} con {self.guild.id}")

    async def on_message(self, message: dc.Message):
        if message.author == self.user:
            return
        elif message.content == 'errorsito':
            raise dc.DiscordException

        if message.content.startswith('el_pepe'):
            if time.monotonic() - self.timer_pepe >= 10:
                await message.channel.send('el pepe si recibiese una notificación: el wasap!')
                await message.channel.send('el_pepe')
                self.timer_pepe = time.monotonic()
            else:
                await message.channel.send(f"Faltan {int(10 - time.monotonic() + self.timer_pepe)} [s] para volver a enviar el mensaje.")
                await message.author.create_dm()
                await message.author.dm_channel.send(message.content)
        await self.process_commands(message)
    
    async def on_error(self, event, *args, **kwards):
        with open("error.log", "a") as file:
            if event == "on_message":
                file.write(f"Error con el mensaje: {args[0]}\n")
                print(f"Error registado: Mensaje lanzó excepción. Autor: {args[0].author.name}")
            else:
                raise
    
    async def setup_hook(self):
        await self.load_extension("gd_cog")
        await self.load_extension("refresh_cog")

        server = dc.Object(id=self.GUILD_ID)
        #self.tree.copy_global_to(guild=server)
        await self.tree.sync(guild=server)
