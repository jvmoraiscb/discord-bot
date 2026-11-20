import json
from pathlib import Path

LOCALES_DIR = Path(__file__).parent.parent / "locales"

SUPPORTED_LANGUAGES = {"en-US", "pt-BR"}
DEFAULT_LANGUAGE = "en-US"

translations = {}

for file in LOCALES_DIR.glob("*.json"):
    with open(file, "r", encoding="utf-8") as f:
        translations[file.stem] = json.load(f)


def get_text(language, key, **kwargs):
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE

    keys = key.split(".")
    value = translations[language]

    for item in keys:
        value = value[item]

    if not isinstance(value, str):
        raise ValueError(f"Translation key '{key}' does not contain a string")

    return value.format(**kwargs)