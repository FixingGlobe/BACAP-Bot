from typing import List

import disnake
from disnake.ext import commands
from Embeds.AdvancementEmbed import AdvancementEmbed
from Advancement import Advancement
from AdvancementUtils import PathPairs
import random

advancement_keys = list(PathPairs().bacap_name_pairs.keys())


async def autocomplete_advancement_name(inter: disnake.ApplicationCommandInteraction, user_input: str) -> List[str]:
    if not user_input:
        return random.choices(advancement_keys, k=25)

    names = []
    for name in advancement_keys:
        if user_input in name.lower():
            names.append(name)
            if len(names) == 25:
                break
    return names


async def autocomplete_advancement_description(inter: disnake.ApplicationCommandInteraction, user_input: str) -> List[str]:
    if not user_input:
        return random.choices(advancement_keys, k=25)

    names = []
    for name in advancement_keys:
        if user_input in name.lower():
            names.append(name)
            if len(names) == 25:
                break
    return names


class AdvancementInfo(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="advancement",
        description="Returns advancement by name"
    )
    async def advancement_info(self,
                               inter: disnake.ApplicationCommandInteraction,
                               adv_name: str = commands.Param(
                                   name="name",
                                   description="Name of advancement to find",
                                   autocomplete=autocomplete_advancement_name,
                                   max_length=32,
                                   required=False
                               ),
                               adv_description: str = commands.Param(
                                   name="description",
                                   description="Description of advancement to find",
                                   autocomplete=autocomplete_advancement_description,
                                   required=False
                               )
                               ):
        if not adv_description and adv_name:
            await inter.response.send_message("Empty Request")
        if not adv_path:
            # TODO add good embed for this
            await inter.response.send_message("NO ADV")
        await inter.response.send_message(embed=AdvancementEmbed(Advancement(adv_path)).embed)


def setup(bot: commands.Bot):
    bot.add_cog(AdvancementInfo(bot))
