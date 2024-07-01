import os

import disnake

import Utils
from Trophy import Trophy


class TrophyEmbed:
    def __init__(self, trophy: Trophy):
        self.trophy = trophy
        self._embed = disnake.Embed(
            title=trophy.name,
            description=f"**{trophy.description}**",
            color=trophy.color if trophy.color else 0xDCDDDC
        )

        trophy_icon = f"assets/textures/{trophy.item_id}.png"
        if os.path.exists(trophy_icon):
            self._embed.set_thumbnail(file=disnake.File(trophy_icon))

        if trophy.advancement_name:
            self._embed.add_field(name='Awarded for:', value=trophy.advancement_name)

        if trophy.enchantments:
            print(trophy.enchantments)

    @property
    def embed(self):
        return self._embed
