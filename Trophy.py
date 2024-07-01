from typing import Optional, List
import re

import Utils
from Utils import read_text_file


class Trophy:
    _pattern_bacap = re.compile(
        r"give @s (?P<item_id>.*?)\[item_name='{\"translate\":\"(?P<trophy_name>.*?)\".*?\"color\":\"(?P<trophy_name_color>.*?)\".*?lore=\[(?P<trophy_description>('.*?{\"translate\":\".*?\",\"color\":\".*?\"}.*?',)*).*?\"Awarded for achieving.*?}.*?\"translate\":\"(?P<adv_name>.*?)\".*?color\":\"(?P<adv_color>.*?)\""
    )
    _pattern_bacaped = re.compile(
        r"give @s (?P<item_id>.*?)\[.*?custom_name='{.*?\"color\":\"(?P<trophy_name_color>.*?)\".*?\"translate\":\"(?P<trophy_name>.*?)\".*?lore=\[(?P<trophy_description>('{\"color\":.*?\".*?\",.*?\"translate\":.*?\".*?\"}',)*).*?\"Awarded for achieving.*?}.*?color\":\"(?P<adv_color>.*?)\",\"translate\":\"(?P<adv_name>.*?)\"}")
    _pattern_summon = re.compile(
        r".*?Item:{id:\"(?P<item_id>.*?)\".*?lore\": \[(?P<trophy_description>('{\"color\":\".*?\",\"translate\":\".*?\"}')*).*?\"Awarded for achieving.*?color\":\"(?P<adv_color>.*?)\".*?\"translate\":\"(?P<adv_name>.*?)\".*?custom_name\": '{.*?\"color\":\"(?P<trophy_name_color>.*?)\".*?\"translate\":\"(?P<trophy_name>.*?)\"")
    _pattern_to_parse_desc = re.compile(r"\"translate\":\s*\"(?!enchantment\.minecraft)(.*?)\"")
    _pattern_to_parse_ench = re.compile(r"enchantments={levels:{(\".*?\":\d*)*}")

    def __init__(self, trophy_file: str):
        """
        Инициализирует объект Trophy

        :param trophy_file: Путь к файлу с описанием трофея.
        """
        try:
            trophy_text = read_text_file(trophy_file)
        except IOError as e:
            raise ValueError(f"Error reading trophy file: {e}")

        self._trophy = self._parse_trophy(trophy_text)
        self._trophy["trophy_description"] = "".join(self._trophy.get("trophy_description", "")) or None
        if self._trophy.get("trophy_name_color"):
            self._trophy["trophy_name_color"] = Utils.hex_to_int(self._trophy["trophy_name_color"])

    def _parse_trophy(self, text: str) -> dict:
        """
        Парсит текст трофея и извлекает информацию с помощью регулярных выражений.

        :param text: Текст трофея.
        :return: Словарь с информацией о трофее.
        """
        for pattern in (self._pattern_bacaped, self._pattern_bacap, self._pattern_summon):
            match = re.search(pattern, text)
            if match:
                trophy_data = match.groupdict()
                trophy_data["enchantments"] = re.findall(self._pattern_to_parse_ench, text)
                trophy_data["trophy_description"] = re.findall(self._pattern_to_parse_desc, trophy_data.get("trophy_description", ""))
                return trophy_data
        return {}

    @property
    def name(self) -> Optional[str]:
        return self._trophy.get("trophy_name")

    @property
    def color(self) -> Optional[int]:
        return self._trophy.get("trophy_name_color")

    @property
    def enchantments(self) -> Optional[List[str]]:
        return self._trophy.get("enchantments")

    @property
    def description(self) -> Optional[str]:
        return self._trophy.get("trophy_description")

    @property
    def advancement_name(self) -> Optional[str]:
        return self._trophy.get("adv_name")

    @property
    def item_id(self) -> Optional[str]:
        return self._trophy.get("item_id")

    @property
    def trophy(self):
        return self._trophy
