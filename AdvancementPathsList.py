import os
import json
import timeit
from typing import List, Tuple, Optional


class AdvancementPathsList:
    _instance = None
    _tabs: Tuple[str] = ('adventure', 'animal', 'bacap', 'biomes', 'building', 'challenges', 'enchanting',
                         'end', 'farming', 'mining', 'monsters', 'nether', 'potion', 'redstone', 'statistics', 'weaponry')

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._bacap_advancements = []
            cls._instance._bacaped_advancements = []

            cls._instance._bacap_base_paths = (
                os.path.join('bacap', 'data', 'blazeandcave', 'advancement'),
                os.path.join('bacap', 'data', 'minecraft', 'advancement')
            )
            cls._instance._bacaped_base_paths = (
                os.path.join('bacaped', 'data', 'bacaped', 'advancement'),
            )

            cls._instance.__generate_paths()
        return cls._instance

    def __generate_paths(self):
        self.__generate_paths_for_base_paths(self._bacap_base_paths, self._bacap_advancements)
        self.__generate_paths_for_base_paths(self._bacaped_base_paths, self._bacaped_advancements)

    def __generate_paths_for_base_paths(self, base_paths, advancements_list):
        for base_path in base_paths:
            for root, dirs, files in os.walk(base_path):
                if 'technical' in dirs:
                    dirs.remove('technical')
                for file in files:
                    file_path = os.path.join(root, file)
                    if self.__check_json_file(file_path):
                        advancements_list.append(file_path)

    @staticmethod
    def __check_json_file(file_path):
        try:
            with open(file_path, encoding="UTF-8") as f:
                advancement_data = json.load(f)
                if 'display' not in advancement_data:
                    return False
        except (IOError, ValueError, KeyError) as e:
            print(f"Ошибка в файле {file_path}: {str(e)}")
            return False
        return True

    @property
    def all_bacap_advancements(self) -> List[str]:
        return self._bacap_advancements

    @property
    def all_bacaped_advancements(self) -> List[str]:
        return self._bacaped_advancements

    @property
    def all_advancements(self) -> List[str]:
        """
        :return: All advancements in all extensions
        """
        return self._bacap_advancements + self._bacaped_advancements


if __name__ == '__main__':
    print(AdvancementPathsList().all_bacap_advancements)
    print(AdvancementPathsList().get_advancements_from_tab(tab="building"))

    num_runs = 10000
    elapsed_time = timeit.timeit("AdvancementPathsList().get_advancements_from_tab('adventure')",
                                 setup="from __main__ import AdvancementPathsList",
                                 number=num_runs)
    average_time = elapsed_time / num_runs

    print(f"Время выполнения {num_runs} раз: {elapsed_time} секунд.")
    print(f"Среднее время выполнения: {average_time} секунд.")
