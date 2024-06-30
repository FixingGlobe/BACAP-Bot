import json
import os
from typing import Dict, List, Optional, Tuple

from AdvancementPathsList import AdvancementPathsList


class PathPairs:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._bacap_names_paths_pairs = {}
            cls._instance._bacaped_names_paths_pairs = {}
            cls._instance._bacap_descs_paths_pairs = {}
            cls._instance._bacaped_descs_paths_pairs = {}

            cls._instance.__generate_names()
            cls._instance.__generate_desc()

        return cls._instance

    def __generate_names(self):
        self.__generate_names_for_paths(AdvancementPathsList().all_bacap_advancements, self._bacap_names_paths_pairs)
        self.__generate_names_for_paths(AdvancementPathsList().all_bacaped_advancements, self._bacaped_names_paths_pairs)

    def __generate_desc(self):
        self.__generate_descs_for_paths(AdvancementPathsList().all_bacap_advancements, self._bacap_descs_paths_pairs)
        self.__generate_descs_for_paths(AdvancementPathsList().all_bacaped_advancements, self._bacaped_descs_paths_pairs)

    @staticmethod
    def __generate_names_for_paths(base_paths, advancements_names) -> None:
        for file_path in base_paths:
            with open(file_path, encoding='utf-8') as file:
                json_data = json.load(file)
                advancements_names[json_data["display"]["title"]["translate"]] = file_path

    @staticmethod
    def __generate_descs_for_paths(base_paths, advancements_desc) -> None:
        for file_path in base_paths:
            with open(file_path, encoding='utf-8') as file:
                json_data = json.load(file)
                advancements_desc[json_data["display"]["description"]["translate"]] = file_path

    @property
    def bacap_name_pairs(self) -> Dict[str, str]:
        return self._bacap_names_paths_pairs

    @property
    def bacaped_name_pairs(self) -> Dict[str, str]:
        return self._bacaped_names_paths_pairs

    @property
    def all_name_pairs(self) -> Dict[str, str]:
        """
        :return: All advancement names in all extensions
        """
        return self._bacap_names_paths_pairs | self._bacaped_names_paths_pairs

    @property
    def bacap_desc_pairs(self) -> Dict[str, str]:
        return self._bacap_descs_paths_pairs

    @property
    def bacaped_desc_pairs(self) -> Dict[str, str]:
        return self._bacap_descs_paths_pairs

    @property
    def all_desc_pairs(self) -> Dict[str, str]:
        """
         :return: All advancement descriptions in all extensions
         """
        return self._bacap_descs_paths_pairs | self._bacaped_descs_paths_pairs


class AdvancementCatalog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._bacap_tab_catalog = {}
            cls._instance._bacaped_tab_catalog = {}
            cls._instance._bacap_adv_type_catalog = {}
            cls._instance._bacaped_adv_type_catalog = {}

            cls._instance.__generate_catalogs()
        return cls._instance

    def __generate_catalogs(self):
        self.__generate_tab_catalog_for_path(AdvancementPathsList().all_bacap_advancements, self._bacap_tab_catalog)
        self.__generate_tab_catalog_for_path(AdvancementPathsList().all_bacaped_advancements, self._bacaped_tab_catalog)
        self.__generate_adv_type_catalog_for_path(AdvancementPathsList().all_bacap_advancements, self._bacap_adv_type_catalog)
        self.__generate_adv_type_catalog_for_path(AdvancementPathsList().all_bacaped_advancements, self._bacaped_adv_type_catalog)

    @staticmethod
    def __generate_tab_catalog_for_path(base_paths: list, catalog: dict) -> None:
        for file_path in base_paths:
            tab = get_tab_from_path(file_path)
            if tab in catalog:
                catalog[tab].append(file_path)
            else:
                catalog[tab] = [file_path]

    @staticmethod
    def __generate_adv_type_catalog_for_path(base_paths: list, catalog: dict) -> None:
        for file_path in base_paths:
            with open(file_path, encoding='utf-8') as file:
                json_data = json.load(file)
                adv_type = determine_advancement_type(json_data)
                if adv_type in catalog:
                    catalog[adv_type].append(file_path)
                else:
                    catalog[adv_type] = [file_path]

    def get_bacap_advancements_by_tab(self, tab: str) -> Optional[List[str]]:
        return self._bacap_tab_catalog.get(tab, None)

    def get_bacaped_advancements_by_tab(self, tab: str) -> Optional[List[str]]:
        return self._bacaped_tab_catalog.get(tab, None)

    def get_bacap_advancements_by_type(self, adv_type: str) -> Optional[List[str]]:
        return self._bacap_adv_type_catalog.get(adv_type, None)

    def get_bacaped_advancements_by_type(self, adv_type: str) -> Optional[List[str]]:
        return self._bacaped_adv_type_catalog.get(adv_type, None)


def get_tab_from_path(file_path: str) -> str:
    return file_path.split(os.sep)[-2]


def determine_advancement_type(advancement: dict) -> Optional[str]:
    frame = advancement['display'].get("frame", None)
    description_color = advancement['display']['description'].get("color", None)

    color_to_type = {
        "yellow": "milestone",
        "gold": "advancement_legend",
        "#FF2A2A": "super_challenge",
        "light_purple": "hidden"
    }
    adv_type = color_to_type.get(description_color, None)
    if adv_type:
        return adv_type

    if frame:
        return frame

    return None


advancement_tabs: Tuple[str, ...] = ('adventure', 'animal', 'bacap', 'biomes', 'building', 'challenges', 'enchanting',
                                     'end', 'farming', 'mining', 'monsters', 'nether', 'potion', 'redstone', 'statistics', 'weaponry')

advancement_types: Tuple[str, ...] = ("task", "goal", "challenge", "super_challenge", "milestone", "advancement_legend", "hidden")

advancement_color = {"task": 0x54fc54, "goal": 0x74defc, "challenge": 0xa800a8, "hidden": 0xfc54fc,
                     "super_challenge": 0xfc2929, "milestone": 0xfcfc54, "advancement_legend": 0xfca800}

if __name__ == "__main__":
    print(determine_advancement_type(json.load(open(r"bacap\data\blazeandcave\advancement\end\good_luck_getting_this_one.json"))))
