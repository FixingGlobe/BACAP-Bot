import discord
from discord import ButtonStyle

from Advancement import Advancement


class ParentButton(discord.ui.Button):
    def __init__(self, parent: Advancement):
        super().__init__(label="Parent Advancement", style=ButtonStyle.green)
        self.parent = parent

    async def callback(self, inter: discord.ApplicationContext):
        from Messages.AdvancementMessage import AdvancementMessage
        await AdvancementMessage(inter=inter, advancement=self.parent).send()
        self.disabled = True
        await inter.message.edit(view=self.view)
