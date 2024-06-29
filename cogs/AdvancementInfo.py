from typing import List

import disnake
from disnake.ext import commands
from AdvancementEmbed import AdvancementEmbed
from Advancement import Advancement
from AdvancementUtils import AdvancementNames
import random

advancement_keys = list(AdvancementNames().all_bacap_advancement_names.keys())


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


class AdvancementInfo(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="advancement", description="Returns advancement by name")
    async def advancement_info(self, inter: disnake.ApplicationCommandInteraction,
                               adv_name: str = commands.Param(name="advancement_name", autocomplete=autocomplete_advancement_name, max_length=32)
                               ):
        adv_path = AdvancementNames().all_bacap_advancement_names.get(adv_name)
        if not adv_path:
            # TODO add good embed for this
            await inter.response.send_message("NO ADV")
        await inter.response.send_message(embed=AdvancementEmbed(Advancement(adv_path)).embed)


def setup(bot: commands.Bot):
    bot.add_cog(AdvancementInfo(bot))
