import discord as dc
from dotenv import load_dotenv
import os
from gd_bot import GDQuiz
from typing import Literal, Optional
from discord.ext import commands

if __name__ == "__main__":

    load_dotenv("credentials.env")
    TOKEN = os.getenv("TOKEN")
    intents = dc.Intents.default()
    intents.message_content = True

    client = GDQuiz(intents=intents, command_prefix='$')

    # Fuerza limpieza del tree de slash commands, trozo hecho por la IA
    @client.command(name="sync")
    @commands.is_owner() # Solo tú puedes usar este comando
    async def sync(ctx: commands.Context, spec: Optional[Literal["clean", "global", "local"]] = None):
    
        server = dc.Object(id=client.GUILD_ID) # O ctx.guild

        if spec == "clean":
            # 1. Borramos todo rastro de los globales
            client.tree.clear_commands(guild=None)
            await client.tree.sync()
            
            # 2. Borramos todo rastro de los locales (por si acaso)
            client.tree.clear_commands(guild=server)
            await client.tree.sync(guild=server)
            
            await ctx.send("🧹 Árbol de comandos borrado. Reinicia el bot para recargar.")
            return
            
        elif spec == "local":
            # Sincronizamos solo en este servidor
            client.tree.copy_global_to(guild=server)
            synced = await client.tree.sync(guild=server)
            await ctx.send(f"✅ Sincronizados {len(synced)} comandos locales.")
            return

        # Sincronización normal global
        synced = await client.tree.sync()
        await ctx.send(f"🌍 Sincronizados {len(synced)} comandos globalmente (puede tardar en aparecer).")
    client.run(TOKEN)
