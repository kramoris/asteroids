import json
from pathlib import Path


DEFAULT_SETTINGS = {
    "screen_width": 1280,
    "screen_height": 720,
    "fps_limit": 60,
}

SETTINGS_FILE = Path("settings.json")

SETTING_RULES = {
    "screen_width": {"type": int, "min": 640, "max": 3840, "step": 160},
    "screen_height": {"type": int, "min": 480, "max": 2160, "step": 90},
    "fps_limit": {"type": int, "min": 30, "max": 240, "step": 30},
}


def _coerce_and_validate(key, value):
    rule = SETTING_RULES[key]
    expected_type = rule["type"]

    if expected_type is int and isinstance(value, bool):
        return DEFAULT_SETTINGS[key]

    if not isinstance(value, expected_type):
        return DEFAULT_SETTINGS[key]

    if "min" in rule and value < rule["min"]:
        return DEFAULT_SETTINGS[key]

    if "max" in rule and value > rule["max"]:
        return DEFAULT_SETTINGS[key]

    return value


def load_settings():
    settings = DEFAULT_SETTINGS.copy()

    if not SETTINGS_FILE.exists():
        save_settings(settings)
        return settings

    try:
        with SETTINGS_FILE.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
    except (OSError, json.JSONDecodeError):
        save_settings(settings)
        return settings

    if not isinstance(loaded, dict):
        save_settings(settings)
        return settings

    for key in DEFAULT_SETTINGS:
        if key in loaded:
            settings[key] = _coerce_and_validate(key, loaded[key])

    save_settings(settings)
    return settings


def save_settings(settings):
    SETTINGS_FILE.write_text(
        json.dumps(settings, indent=4, sort_keys=True),
        encoding="utf-8",
    )


def reset_settings():
    settings = DEFAULT_SETTINGS.copy()
    save_settings(settings)
    return settings


def get_setting_options(key):
    return SETTING_RULES[key]
