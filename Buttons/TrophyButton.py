import discord
from discord import ButtonStyle

from Trophy import Trophy
from Embeds.TrophyEmbed import TrophyEmbed


class TrophyButton(discord.ui.Button):
    def __init__(self, trophy: Trophy):
        super().__init__(label="Trophy details", style=ButtonStyle.blurple)
        self.trophy = trophy

    async def callback(self, inter: discord.ApplicationContext):
        embed = TrophyEmbed(trophy=self.trophy)
        await inter.response.send_message(embed=embed.embed, file=embed.icon)
        self.disabled = True
        await inter.message.edit(view=self.view)
