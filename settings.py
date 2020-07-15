"""User Settings."""
import json
from dataclasses import dataclass

SETTINGS_FILE = 'settings.json'


@dataclass
class Settings:
    """Container for user defined settings."""
    file_location: str
    output_folder: str


def get_settings() -> Settings:
    """Open user settings file and return python class representation."""
    with open(SETTINGS_FILE) as f:
        data = json.load(f)
        return Settings(
            file_location=data.get('file_location'),
            output_folder=data.get('output_folder'),
        )
