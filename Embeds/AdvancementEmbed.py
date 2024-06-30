import os

import disnake
from Advancement import Advancement
import Utils
from AdvancementUtils import advancement_color

class AdvancementEmbed:
    def __init__(self, advancement: Advancement):

        self._embed = disnake.Embed(
            title=advancement.name,
            description=f"**{advancement.description}**",
            color=advancement_color.get(advancement.adv_type, 0xDCDDDC),

        )

        advancement_icon = f"assets/textures/{Utils.cut_namespace(advancement.icon_id)}.png"
        if os.path.exists(advancement_icon):
            self._embed.set_thumbnail(file=disnake.File(advancement_icon))

        self._embed.add_field(name='Tab:', value=advancement.tab.capitalize())

        if advancement.parent:
            if parent_name := Advancement(advancement.internal_parent).name:
                self._embed.add_field(name='Parent', value=parent_name)

        if advancement.expansion:
            self._embed.add_field(name='Expansion', value=advancement.expansion.capitalize())

        self._embed.add_field(name='Hidden?', value=advancement.hidden)

        if advancement.experience:
            self._embed.add_field(name='Experience:', value=advancement.experience)

        if advancement.reward:
            reward_item = Utils.cut_namespace(advancement.reward["item"].replace('_', " ")).title()
            self._embed.add_field(name='Reward:', value=f"{reward_item}: {advancement.reward['count']}")

        if advancement.trophy:
            self._embed.add_field(name='Trophy:', value=advancement.trophy)

    @property
    def embed(self):
        return self._embed
