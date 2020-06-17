import json
from dataclasses import dataclass

SETTINGS_FILE = 'settings.json'


@dataclass
class Settings:
    """Container for user defined settings."""
    file_location: str


def get_settings() -> Settings:
    with open(SETTINGS_FILE) as f:
        data = json.load(f)
        return Settings(file_location=data.get('file_location'))
