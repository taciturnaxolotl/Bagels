import warnings
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings_yaml import YamlBaseSettings

from bagels.locations import config_file


class Defaults(BaseModel):
    period: Literal["day", "week", "month", "year"] = "day"
    first_day_of_week: int = Field(ge=0, le=6, default=6)

class InsightsHotkeys(BaseModel):
    toggle_use_account: str = "\\"
    
class DatemodeHotkeys(BaseModel):
    go_to_day: str = "g"

class HomeHotkeys(BaseModel):
    categories: str = "c"
    new_transfer: str = "t"
    toggle_splits: str = "s"
    display_by_date: str = "q"
    display_by_person: str = "w"
    cycle_offset_type: str = "."
    toggle_income_mode: str = "/"
    select_prev_account: str = "["
    select_next_account: str = "]"
    insights: InsightsHotkeys = InsightsHotkeys()
    datemode: DatemodeHotkeys = DatemodeHotkeys()

class RecordModalHotkeys(BaseModel):
    new_split: str = "ctrl+a"
    new_paid_split: str = "ctrl+s"
    delete_last_split: str = "ctrl+d"

class CategoriesHotkeys(BaseModel):
    new_subcategory: str = "s"

class Hotkeys(BaseModel):
    new: str = "a"
    delete: str = "d"
    edit: str = "e"
    toggle_jump_mode: str = "v"
    home: HomeHotkeys = HomeHotkeys()
    record_modal: RecordModalHotkeys = RecordModalHotkeys()
    categories: CategoriesHotkeys = CategoriesHotkeys()

class Symbols(BaseModel):
    line_char: str = "│"
    finish_line_char: str = "╰"
    split_paid: str = "✓"
    split_unpaid: str = "⨯"
    category_color: str = "●"
    amount_positive: str = "+"
    amount_negative: str = "-"

class State(BaseModel):
    theme: str = "posting"

class Config(YamlBaseSettings):
    hotkeys: Hotkeys = Hotkeys()
    symbols: Symbols = Symbols()
    model_config = SettingsConfigDict(
        yaml_file=str(config_file()),
        yaml_file_encoding='utf-8',
    )
    defaults: Defaults = Defaults()
    state: State = State()

    @classmethod
    def get_default(cls):
        # Create a default instance without reading from file
        return cls.model_construct(
            hotkeys=Hotkeys(),
            symbols=Symbols(),
            defaults=Defaults(),
            state=State()
        )

# Only try to load from file if it exists
config_path = config_file()

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    CONFIG = Config.get_default() if not config_path.exists() else Config() # ignore warnings about empty env file

def write_state(key: str, value: Any) -> None:
    """Write a state value to the config.yaml file."""
    try:
        with open(config_file(), "r") as f:
            config = yaml.safe_load(f) or {}
    except FileNotFoundError:
        config = {}
    
    if "state" not in config:
        config["state"] = {}
    config["state"][key] = value
    
    with open(config_file(), "w") as f:
        yaml.dump(config, f, default_flow_style=False)