import os
import discord
import logging

from pathlib import Path
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from utils.translator import BotTranslator
from utils.localization import get_localized_text
from database import get_guild_settings

from database.connection import (
    initialize_database,
    close_database
)

DEFAULT_LANGUAGE = "en_US"
DEFAULT_LOG_LEVEL = logging.INFO

Path("logs").mkdir(exist_ok=True)

discord.utils.setup_logging(
    level=DEFAULT_LOG_LEVEL
)

file_handler = RotatingFileHandler(
    "logs/bot.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)

file_handler.setFormatter(
    logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{"
    )
)

logging.getLogger().addHandler(file_handler)

logger = logging.getLogger("discord_bot")

load_dotenv()

class DiscordBotCommandTree(app_commands.CommandTree):
    async def on_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if interaction.guild_id is None:
            language = DEFAULT_LANGUAGE
        else:
            settings = await get_guild_settings(interaction.guild_id)
            language = settings.bot_language

        if isinstance(error, app_commands.MissingPermissions):
            message = get_localized_text(
                language,
                "errors.missing_permissions"
            )
        elif isinstance(error, app_commands.CheckFailure):
            message = get_localized_text(
                language,
                "errors.check_failure"
            )
        else:
            message = get_localized_text(
                language,
                "errors.unexpected"
            )

        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
            return
        
        await interaction.response.send_message(message, ephemeral=True)

class DiscordBot(commands.Bot):
    def __init__(self):
        intents=discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix="!",
            intents=intents,
            tree_cls=DiscordBotCommandTree
        )

    async def setup_hook(self):
        await self.tree.set_translator(BotTranslator())
        await initialize_database()
        await self.load_extension("cogs.bot")
        await self.tree.sync()

    async def close(self):
        await super().close()
        await close_database()

    async def on_ready(self):
        logger.info("DiscordBot connected as %s", self.user)
        logger.info("Connected to %s guild(s):", len(self.guilds))
        for guild in self.guilds:
            logger.info("Connected to guild: %s (%s)", guild.name, guild.id)

    async def on_guild_join(self, guild: discord.Guild):
        logger.info("Joined guild: %s (%s)", guild.name, guild.id)

    async def on_guild_remove(self, guild: discord.Guild):
        logger.info("Left guild: %s (%s)", guild.name, guild.id)

client = DiscordBot()


client.run(os.getenv("DISCORD_TOKEN"))
