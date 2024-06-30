import time
from typing import List

import disnake
from disnake.ext import commands
from Embeds.AdvancementEmbed import AdvancementEmbed
from Advancement import Advancement
from AdvancementUtils import PathPairs
import random
import Embeds.PreMadeEmbeds as Emb

from Embeds.EmptyRequestEmbed import EmptyRequestEmbed

advancement_name_keys = tuple(PathPairs().bacap_name_pairs.keys())
advancement_desc_keys = tuple(PathPairs().bacap_desc_pairs.keys())


async def autocomplete_advancement_name(inter: disnake.ApplicationCommandInteraction, user_input: str) -> List[str]:
    if not user_input:
        return random.choices(advancement_name_keys, k=10)

    names = []
    lowered_user_input = user_input.lower()
    for name in advancement_name_keys:
        if lowered_user_input in name.lower():
            names.append(name)
            if len(names) == 10:
                break
    return names


async def autocomplete_advancement_description(inter: disnake.ApplicationCommandInteraction, user_input: str) -> List[str]:
    if not user_input:
        return random.choices(advancement_desc_keys, k=10)

    descs = []
    lowered_user_input = user_input.lower()
    for desc in advancement_name_keys:
        if lowered_user_input in desc.lower():
            descs.append(desc)
            if len(descs) == 10:
                break
    return descs


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
                                   default=None
                               ),
                               adv_description: str = commands.Param(
                                   name="description",
                                   description="Description of advancement to find",
                                   autocomplete=autocomplete_advancement_description,
                                   default=None
                               )
                               ):
        if not adv_description and not adv_name:
            return await inter.response.send_message(
                embed=EmptyRequestEmbed(title="Empty Request",
                                        description="Use `name` or `description` parameters").embed)

        if adv_name:
            path = PathPairs().bacap_name_pairs.get(adv_name, None)
            if not path:
                return await inter.response.send_message(embed=Emb.bad_request)
            await inter.response.send_message(embed=AdvancementEmbed(Advancement(path)).embed)

        if adv_description:
            path = PathPairs().bacap_desc_pairs.get(adv_description)
            if not path:
                return await inter.response.send_message(embed=Emb.bad_request)
            await inter.response.send_message(embed=AdvancementEmbed(Advancement(path)).embed)


def setup(bot: commands.Bot):
    bot.add_cog(AdvancementInfo(bot))
