import os

import disnake
from Advancement import Advancement
import Utils


class AdvancementEmbed:
    def __init__(self, advancement: Advancement):

        advancement_color = {"task": 0x54fc54, "goal": 0x74defc, "challenge": 0xa800a8, "hidden": 0xfc54fc,
                             "super_challenge": 0xfc2929, "milestone": 0xfcfc54, "advancement_legend": 0xfca800}

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
