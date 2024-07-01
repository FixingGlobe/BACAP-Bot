import discord

from Embeds.BaseEmbed import BaseEmbed


class EmptyRequestEmbed(BaseEmbed):
    def __init__(self, title: str, description: str, color: int = 0xF25C89, icon: str = "barrier", **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.description = f"**{description}**"
        self.color = color

        self._set_file(item_id=icon)
