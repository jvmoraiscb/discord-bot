import os
import discord

from discord.ext import commands
from dotenv import load_dotenv
from utils.translator import BotTranslator

from database.connection import (
    initialize_database,
    close_database
)

load_dotenv()

intents=discord.Intents.default()
intents.message_content = True

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):
        await self.tree.set_translator(BotTranslator())
        
        await initialize_database()

        await self.load_extension("cogs.bot")

        await self.tree.sync()

    async def close(self):
        await super().close()
        await close_database()

bot = DiscordBot()

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))
