import os
from typing import Optional

import discord
from Advancement import Advancement
import Utils
from AdvancementUtils import advancement_color


class AdvancementEmbed:
    def __init__(self, advancement: Advancement):

        self._embed = discord.Embed(
            title=advancement.name,
            description=f"**{advancement.description}**",
            color=advancement_color.get(advancement.adv_type, 0xDCDDDC),

        )
        icon = Utils.cut_namespace(advancement.icon_id)
        advancement_icon = f"assets/textures/{icon}.png"

        self._file = None
        if os.path.exists(advancement_icon):
            self._file = discord.File(advancement_icon, filename=f"{icon}.png")
            self._embed.set_thumbnail(url=f"attachment://{icon}.png")

        self._embed.add_field(name='Tab:', value=advancement.tab.capitalize())

        if advancement.parent:
            if parent_name := Advancement(advancement.internal_parent).name:
                self._embed.add_field(name='Parent', value=parent_name)

        if advancement.expansion:
            self._embed.add_field(name='Expansion', value=advancement.expansion.capitalize())

        self._embed.add_field(name='Hidden?', value=str(advancement.hidden))

        if advancement.experience:
            self._embed.add_field(name='Experience:', value=str(advancement.experience))

        if advancement.reward:
            reward_item = Utils.cut_namespace(advancement.reward["item"].replace('_', " ")).title()
            self._embed.add_field(name='Reward:', value=f"{reward_item}: {advancement.reward['count']}")

        if advancement.trophy:
            self._embed.add_field(name='Trophy:', value=advancement.trophy.name)

    @property
    def embed(self) -> discord.Embed:
        return self._embed

    @property
    def icon(self) -> Optional[discord.File]:
        return self._file
