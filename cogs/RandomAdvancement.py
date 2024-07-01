import random

import discord
import discord.ext.commands as commands

import Utils
from AdvancementPathsList import AdvancementPathsList
from Embeds.PreMadeEmbeds import bad_params
from Advancement import Advancement
from AdvancementUtils import advancement_tabs as adv_tabs, advancement_types as adv_types, AdvancementCatalog
from Messages.AdvancementMessage import AdvancementMessage


class RandomAdvancement(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="random_advancement",
        description="Returns a random advancement by criteria"
    )
    async def random_advancement(
            self,
            inter: discord.ApplicationContext,
            tab: str = discord.Option(
                default=None,
                name="tab",
                description="Tab of advancement. If there are no advancements matching the parameter, it will be ignored",
                choices=list(adv_tabs)  # Список выбора для параметра tab
            ),
            adv_type: str = discord.Option(
                default=None,
                name="type",
                description="Type of advancement. If there are no advancements matching the parameter, it will be ignored",
                choices=list(adv_types)  # Список выбора для параметра adv_type
            )):

        if tab or adv_type:  # Если существует какой-то из параметров, используем сортировку
            tab_advancements = AdvancementCatalog().get_bacap_advancements_by_tab(tab)
            type_advancements = AdvancementCatalog().get_bacap_advancements_by_type(adv_type)
            possible_advancements = Utils.set_intersection(tab_advancements, type_advancements)
        else:
            possible_advancements = AdvancementPathsList().all_bacap_advancements  # Иначе выбираем любые достижения

        # Если достижения существуют, создаем случайное и отправляем
        if possible_advancements:
            advancement = Advancement(random.choice(possible_advancements))
            return await AdvancementMessage(inter=inter, advancement=advancement).send()

        # Если нет, то отправляем ошибку
        return await inter.response.send_message(embed=bad_params, file=bad_params.icon)


def setup(bot: commands.Bot):
    bot.add_cog(RandomAdvancement(bot))
