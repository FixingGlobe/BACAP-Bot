import os

import disnake


class EmptyRequestEmbed:
    def __init__(self, title: str, description: str, color: int = 0xF25C89, icon: str = None):
        """

        :param title: Title of error
        :param description: Description of error
        :param color: int 16 based color
        :param icon: minecraft item name without .png ex: barrier, acacia_door
        """
        self._embed = disnake.Embed(
            title=title,
            description=f"**{description}**",
            color=color,
        )
        icon = self.__get_icon_path(icon)
        self._embed.set_thumbnail(file=disnake.File(icon))

    @staticmethod
    def __get_icon_path(icon: str):
        default_icon_path = "assets/textures/barrier.png"
        if icon:
            icon_path = f"assets/textures/{icon}.png"
            if os.path.exists(icon_path):
                return icon_path
        return default_icon_path

    @property
    def embed(self) -> disnake.Embed:
        return self._embed
