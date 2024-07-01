from Advancement import Advancement
import Utils
from AdvancementUtils import advancement_color
from Embeds.BaseEmbed import BaseEmbed


class AdvancementEmbed(BaseEmbed):
    def __init__(self, advancement: Advancement, **kwargs):

        super().__init__(**kwargs)
        self.title = advancement.name
        self.description = f"**{advancement.description}**"
        self.color = advancement_color.get(advancement.adv_type, 0xDCDDDC)

        self._set_file(item_id=advancement.icon_id, on_error_item=None)

        self.add_field(name='Tab:', value=advancement.tab.capitalize())

        if advancement.parent:
            if parent_name := Advancement(advancement.internal_parent).name:
                self.add_field(name='Parent', value=parent_name)

        if advancement.expansion:
            self.add_field(name='Expansion', value=advancement.expansion.capitalize())

        self.add_field(name='Hidden?', value=str(advancement.hidden))

        if advancement.experience:
            self.add_field(name='Experience:', value=str(advancement.experience))

        if advancement.reward:
            reward_item = Utils.cut_namespace(advancement.reward["item"].replace('_', " ")).title()
            self.add_field(name='Reward:', value=f"{reward_item}: {advancement.reward['count']}")

        if advancement.trophy:
            self.add_field(name='Trophy:', value=advancement.trophy.name)
