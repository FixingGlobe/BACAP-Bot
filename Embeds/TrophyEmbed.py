from Trophy import Trophy
from Embeds.BaseEmbed import BaseEmbed


class TrophyEmbed(BaseEmbed):
    def __init__(self, trophy: Trophy, **kwargs):
        super().__init__(**kwargs)
        self.trophy = trophy
        self.title = trophy.name
        self.description = f"**{trophy.description}**"
        self.color = trophy.color if trophy.color else 0xDCDDDC

        self._set_file(trophy.item_id, None)

        if trophy.advancement_name:
            self.add_field(name='Awarded for:', value=trophy.advancement_name)

        if trophy.enchantments:
            print(trophy.enchantments)

