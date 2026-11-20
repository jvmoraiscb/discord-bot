import discord

from discord import app_commands
from discord.ext import commands

from database import set_guild_language
from utils.localization import get_text

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
            app_commands.Choice(name="English (US)", value="en-US"),
            app_commands.Choice(name="Português (Brasil)", value="pt-BR")
        ]
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def language(
        self,
        interaction: discord.Interaction,
        language: app_commands.Choice[str]
    ):
        await set_guild_language(
            interaction.guild_id,
            language.value
        )

        await interaction.response.send_message(
            get_text(
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
