import os
from typing import Optional

import discord

import Utils


class BaseEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _set_file(self, item_id: str, on_error_item: Optional[str] = "barrier"):
        self._file = None
        if item_id:
            icon = self._get_icon_path(item_id, on_error_item)
            icon_name = icon.rsplit(os.sep)[-1]
            print(icon)
            print(icon_name)
            self._file = discord.File(icon, filename=icon_name)
            self.set_thumbnail(url=f"attachment://{icon_name}")

    @staticmethod
    def _get_icon_path(icon: str, default: Optional[str] = "barrier"):
        icon = Utils.cut_namespace(icon)
        if icon:
            icon_path = os.sep.join(["assets", "textures", f"{icon}.png"])
            if os.path.exists(icon_path):
                return icon_path
        if default:
            return f"assets/textures/{default}.png"
        return None

    @property
    def icon(self) -> Optional[discord.File]:
        return self._file
