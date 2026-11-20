from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class GuildSettings(Base):
    __tablename__ = "guild_settings"

    guild_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    bot_language: Mapped[str] = mapped_column(
        String(5),
        default="en-US",
        nullable=False
    )
