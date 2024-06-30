import os

import disnake


class EmptyRequestEmbed:
    def __init__(self, title: str, description: str, color: int = 0xF25C89):
        self._embed = disnake.Embed(
            title=title,
            description=f"**{description}**",
            color=color,
        )

    @property
    def embed(self):
        return self._embed
