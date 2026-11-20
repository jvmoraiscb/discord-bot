from database.connection import async_session
from database.models import GuildSettings

DEFAULT_LANGUAGE = "en-US"

async def get_guild_settings(guild_id: int) -> GuildSettings:
    async with async_session() as session:
        settings = await session.get(
            GuildSettings,
            str(guild_id)
        )

        if settings is None:
            settings = GuildSettings(
                guild_id=str(guild_id),
                bot_language=DEFAULT_LANGUAGE
            )
            session.add(settings)
            await session.commit()
            
        return settings


async def set_guild_language(guild_id: int, language: str):
    async with async_session() as session:
        settings = await session.get(
            GuildSettings,
            str(guild_id)
        )

        if settings is None:
            settings = GuildSettings(
                guild_id=str(guild_id),
                bot_language=language
            )

            session.add(settings)
        else:
            settings.bot_language = language

        await session.commit()