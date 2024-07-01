import os

import discord

import Utils
from Trophy import Trophy


class TrophyEmbed:
    def __init__(self, trophy: Trophy):
        self.trophy = trophy
        self._embed = discord.Embed(
            title=trophy.name,
            description=f"**{trophy.description}**",
            color=trophy.color if trophy.color else 0xDCDDDC
        )

        trophy_icon = f"assets/textures/{trophy.item_id}.png"
        self._file = None
        if os.path.exists(trophy_icon):
            self._file = discord.File(trophy_icon, filename=f"{trophy.item_id}.png")
            self._embed.set_thumbnail(url=f"attachment://{trophy.item_id}.png")

        if trophy.advancement_name:
            self._embed.add_field(name='Awarded for:', value=trophy.advancement_name)

        if trophy.enchantments:
            print(trophy.enchantments)

    @property
    def embed(self):
        return self._embed

    @property
    def icon(self):
        return self._file
