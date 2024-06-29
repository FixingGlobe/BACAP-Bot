import disnake
from disnake.ext import commands
from AdvancementPathsList import AdvancementPathsList
import random
from AdvancementEmbed import AdvancementEmbed
from Advancement import Advancement


class RandomAdvancement(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="random_advancement", description="Returns a random advancement from BACAP")
    async def random_advancement(self, inter: disnake.ApplicationCommandInteraction):
        adv = Advancement(random.choice(AdvancementPathsList().all_bacap_advancements + AdvancementPathsList().all_bacaped_advancements))
        await inter.response.send_message(embed=AdvancementEmbed(adv).embed)


def setup(bot: commands.Bot):
    bot.add_cog(RandomAdvancement(bot))
