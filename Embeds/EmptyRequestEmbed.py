import os

import discord


class EmptyRequestEmbed:
    def __init__(self, title: str, description: str, color: int = 0xF25C89, icon: str = None):
        """

        :param title: Title of error
        :param description: Description of error
        :param color: int 16 based color
        :param icon: minecraft item name without .png ex: barrier, acacia_door
        """
        self._embed = discord.Embed(
            title=title,
            description=f"**{description}**",
            color=color,
        )
        icon = self.__get_icon_path(icon=icon)
        self._file = discord.File(self.__get_icon_path(icon), filename=icon.rsplit("/")[-1])
        self._embed.set_thumbnail(url=f"attachment://{icon}")

    @staticmethod
    def __get_icon_path(icon: str):
        if icon:
            icon_path = f"assets/textures/{icon}.png"
            if os.path.exists(icon_path):
                return icon_path
        return "assets/textures/barrier.png"

    @property
    def embed(self) -> discord.Embed:
        return self._embed

    @property
    def icon(self) -> discord.File:
        return self._file
