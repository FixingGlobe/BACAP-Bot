import discord

from Advancement import Advancement
from Buttons.ParentButton import ParentButton
from Buttons.TrophyButton import TrophyButton
from Embeds.AdvancementEmbed import AdvancementEmbed


class AdvancementMessage:
    def __init__(self, inter: discord.ApplicationContext, advancement: Advancement):
        self._inter = inter
        self._embed = AdvancementEmbed(advancement)
        self._view = discord.ui.View()

        if advancement.internal_parent:
            parent = Advancement(advancement.internal_parent)
            if not parent.hidden:
                self._view.add_item(ParentButton(parent=parent))

        if advancement.trophy:
            if advancement.trophy.name and advancement.trophy.description:
                self._view.add_item(TrophyButton(trophy=advancement.trophy))

    async def send(self):
        return await self._inter.response.send_message(embed=self._embed, view=self._view, file=self._embed.icon)
