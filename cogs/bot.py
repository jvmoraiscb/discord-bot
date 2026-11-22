import discord
import logging

from discord import app_commands
from discord.ext import commands

from database import set_guild_language
from utils.localization import get_localized_text

logger = logging.getLogger(__name__)

class BotCommands(app_commands.Group):
    def __init__(self):
        super().__init__(
            name="bot",
            description=app_commands.locale_str("bot.description")
        )

    @app_commands.command(
        name="language",
        description=app_commands.locale_str("bot.language.description")
    )
    @app_commands.describe(
        language=app_commands.locale_str("bot.language.select_description")
    )
    @app_commands.choices(
        language=[
            app_commands.Choice(
                name=app_commands.locale_str("bot.language.select_en_us"),
                value="en-US"
            ),
            app_commands.Choice(
                name=app_commands.locale_str("bot.language.select_pt_br"),
                value="pt-BR"
            )
        ]
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def language(
        self,
        interaction: discord.Interaction,
        language: app_commands.Choice[str]
    ):
        logger.info("User '%s' used the '/bot language' command in guild '%s' (%s)", interaction.user.name, interaction.guild.name, interaction.guild.id)
        await set_guild_language(
            interaction.guild_id,
            language.value
        )

        await interaction.response.send_message(
            get_localized_text(
                language.value,
                "bot.language.updated_message"
            ),
            ephemeral=True
        )

class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(BotCommands())

async def setup(bot):
    await bot.add_cog(Bot(bot))
