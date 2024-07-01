from typing import List
import random
import discord
from discord.ext import commands

import Embeds.PreMadeEmbeds as Emb
from Advancement import Advancement
from AdvancementUtils import PathPairs
from Embeds.EmptyRequestEmbed import EmptyRequestEmbed
from Messages.AdvancementMessage import AdvancementMessage

advancement_name_keys = tuple(PathPairs().bacap_name_pairs.keys())
advancement_desc_keys = tuple(PathPairs().bacap_desc_pairs.keys())


async def autocomplete_advancement_name(self: discord.AutocompleteContext) -> List[str]:
    user_input = self.options["description"]
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


async def autocomplete_advancement_description(self: discord.AutocompleteContext) -> List[str]:
    user_input = self.options["description"]
    if not user_input:
        return random.choices(advancement_desc_keys, k=10)

    descs = []
    lowered_user_input = user_input.lower()
    for desc in advancement_desc_keys:
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
                               inter: discord.ApplicationContext,
                               adv_name: str = discord.Option(
                                   name="name",
                                   description="Name of advancement to find",
                                   autocomplete=autocomplete_advancement_name,
                                   max_length=32,
                                   default=None
                               ),
                               adv_description: str = discord.Option(
                                   name="description",
                                   description="Description of advancement to find",
                                   autocomplete=autocomplete_advancement_description,
                                   default=None
                               )
                               ):
        if not adv_description and not adv_name:
            error_embed = EmptyRequestEmbed(title="Empty Request",
                                        description="Use `name` or `description` parameters")
            return await inter.response.send_message(
                embed=error_embed, file=error_embed.icon)

        path = PathPairs().bacap_name_pairs.get(adv_name, None) or PathPairs().bacap_desc_pairs.get(adv_description, None)

        if path:
            advancement = Advancement(path)
            return await AdvancementMessage(inter=inter, advancement=advancement).send()
        return await inter.response.send_message(embed=Emb.bad_request, file=Emb.bad_request.icon)


def setup(bot: commands.Bot):
    bot.add_cog(AdvancementInfo(bot))
