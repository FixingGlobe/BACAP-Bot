import json
import os
from typing import List, Dict

from AdvancementPathsList import AdvancementPathsList


class AdvancementNames:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._bacap_names_paths_pairs = {}
            cls._instance._bacaped_names_paths_pairs = {}

            cls._instance.__generate_names()
        return cls._instance

    def __generate_names(self):
        self.__generate_names_for_paths(AdvancementPathsList().all_bacap_advancements, self._bacap_names_paths_pairs)
        self.__generate_names_for_paths(AdvancementPathsList().all_bacaped_advancements, self._bacaped_names_paths_pairs)

    @staticmethod
    def __generate_names_for_paths(base_paths, advancements_names):
        for file_path in base_paths:
            json_data = json.load(open(file_path, encoding='utf-8'))
            advancements_names[json_data["display"]["title"]["translate"]] = file_path

    @property
    def all_bacap_advancement_names(self) -> Dict[str, str]:
        return self._bacap_names_paths_pairs

    @property
    def all_bacaped_advancement_names(self) -> Dict[str, str]:
        return self._bacaped_names_paths_pairs

    @property
    def all_advancements(self) -> Dict[str, str]:
        """
        :return: All advancement names in all extensions
        """
        return self._bacap_names_paths_pairs | self._bacaped_names_paths_pairs
