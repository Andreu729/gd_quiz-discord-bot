import discord as dc
from dotenv import load_dotenv
import os
import time

class GDQuiz(dc.Client):
    load_dotenv("credentials.env")
    GUILD_ID = None
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

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('el_pepe'):
            if time.monotonic() - self.timer_pepe >= 10:
                await message.channel.send('el pepe si recibiese una notificación: el wasap!')
                self.timer_pepe = time.monotonic()
            else:
                await message.channel.send(f"Faltan {int(10 - time.monotonic() + self.timer_pepe)} [s] para volver a enviar el mensaje.")
