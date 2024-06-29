import disnake
from disnake.ext import commands
from Advancements.AdvancementList import AdvancementList
import random
from AdvancementEmbed import AdvancementEmbed
from Advancements.Advancement import Advancement


class RandomAdvancement(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="random_advancement", description="Returns a random advancement from BACAP")
    async def random_advancement(self, inter: disnake.ApplicationCommandInteraction):
        adv = Advancement(random.choice(AdvancementList().bacap_advancements + AdvancementList().bacaped_advancements))
        await inter.response.send_message(embed=AdvancementEmbed(adv).embed)


def setup(bot: commands.Bot):
    bot.add_cog(RandomAdvancement(bot))
