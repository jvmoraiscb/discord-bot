import discord

from discord import app_commands
from utils.localization import get_localized_text

class BotTranslator(app_commands.Translator):
    async def translate(
        self,
        string: app_commands.locale_str,
        locale: discord.Locale,
        context: app_commands.TranslationContext
    ) -> str | None:

        language_map = {
            "en-US": "en_us",
            "pt-BR": "pt_br"
        }

        language = language_map.get(locale.value)

        if language is None:
            return None

        try:
            return get_localized_text(language, string.message)
        except (KeyError, ValueError):
            return None
