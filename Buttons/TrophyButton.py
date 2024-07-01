import disnake
from disnake import ButtonStyle

from Trophy import Trophy
from Embeds.TrophyEmbed import TrophyEmbed


class TrophyButton(disnake.ui.Button):
    def __init__(self, trophy: Trophy):
        super().__init__(label="Trophy details", style=ButtonStyle.blurple)
        self.trophy = trophy

    async def callback(self, inter: disnake.MessageInteraction):
        await inter.response.send_message(embed=TrophyEmbed(trophy=self.trophy).embed)
        self.disabled = True
        await inter.message.edit(view=self.view)
