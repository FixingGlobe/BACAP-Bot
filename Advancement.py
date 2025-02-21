import json
import os
from typing import Optional, Tuple, Dict, TextIO

import AdvancementUtils
from Trophy import Trophy
from AdvancementParsedPaths import AdvancementParsedPaths


class Advancement:
    def __init__(self, advancement_path: str):
        advancement_paths = AdvancementParsedPaths(advancement_path)

        splitted_advancement_path = advancement_paths.advancement.split(os.sep)

        self._internal_name = f'{os.sep}'.join(splitted_advancement_path[2:])

        self._tab = advancement_paths.advancement.split(os.sep)[-2]

        if splitted_advancement_path[0] != "bacap":
            self._expansion = self._internal_name.split("\\")[0]
        else:
            self._expansion = None

        with open(advancement_path, encoding="UTF-8") as advancement_data:
            advancement_json = json.load(advancement_data)
            self._name = advancement_json['display']['title']['translate']
            self._description = advancement_json['display']['description']['translate']
            self._hidden = advancement_json['display'].get('hidden', False)

            self._parent = advancement_json.get('parent', None)
            self._internal_parent = AdvancementParsedPaths.minecraft_parent_to_file_path(advancement_json.get('parent', None))

            self._icon_id = advancement_json['display']["icon"]["id"]

            self._adv_type = AdvancementUtils.determine_advancement_type(advancement_json)

        self._reward, self._reward_count = None, None
        if advancement_paths.reward:
            self._reward, self._reward_count = self.__parse_reward(advancement_paths.reward)

        self._experience = None
        if advancement_paths.experience:
            self._experience = self.__parse_experience(advancement_paths.experience)

        self._trophy = None
        if advancement_paths.trophy:
            self._trophy = Trophy(advancement_paths.trophy)

    @staticmethod
    def __parse_reward(reward_path: str) -> Tuple[Optional[str], Optional[int]]:
        with open(reward_path, encoding="UTF-8") as reward_file:
            first_line = reward_file.readline().strip()  # Читаем первую строку и убираем пробелы
            if first_line:
                reward_line = first_line.split(" ")  # Разделяем строку по пробелам
                try:
                    value = int(reward_line[-1])
                    reward = reward_line[-2].split("[")[0]
                except ValueError:
                    value = 1
                    reward = reward_line[-1].split("[")[0]
                return reward, value
            return None, None

    @staticmethod
    def __parse_experience(experience_path: str) -> int:
        with open(experience_path, encoding="UTF-8") as reward_file:
            first_line = reward_file.readline().strip()  # Читаем первую строку и убираем пробелы
            if first_line:
                experience_line = first_line.split(" ")  # Разделяем строку по пробелам
                try:
                    return int(experience_line[-1])
                except ValueError:
                    return 0

    @staticmethod
    def __read_json_save(stream: TextIO):
        text = stream.read()
        try:
            return json.loads(text)
        except json.decoder.JSONDecodeError:
            return json.loads(text.replace("\\'", ""))
        finally:
            stream.close()

    @property
    def name(self) -> str:
        return self._name

    @property
    def internal_name(self) -> str:
        return self._internal_name

    @property
    def description(self) -> str:
        return self._description

    @property
    def tab(self) -> str:
        return self._tab

    @property
    def hidden(self) -> bool:
        return self._hidden

    @property
    def adv_type(self) -> str:
        return self._adv_type

    @property
    def expansion(self) -> str:
        return self._expansion

    @property
    def reward(self) -> Optional[Dict[str, str | int]]:
        if not self._reward:
            return None
        return {"item": self._reward, "count": self._reward_count}

    @property
    def trophy(self) -> Optional[Trophy]:
        return self._trophy

    @property
    def experience(self) -> Optional[int]:
        return self._experience

    @property
    def parent(self) -> Optional[str]:
        return self._parent

    @property
    def internal_parent(self) -> Optional[str]:
        return self._internal_parent

    @property
    def icon_id(self) -> str:
        return self._icon_id

    def __str__(self):
        return str(self.get_all_properties())

    def get_all_properties(self) -> Dict[str, Optional[Dict[str, str | int]] | str | int | None]:
        return {
            'name': self.name,
            'internal_name': self.internal_name,
            'description': self.description,
            'tab': self.tab,
            'hidden': self.hidden,
            'adv_type': self.adv_type,
            'expansion': self.expansion,
            'reward': self.reward,
            'trophy': self.trophy,
            'experience': self.experience,
            'parent': self.parent,
            'internal_parent': self.internal_parent,
            'icon_id': self.icon_id
        }
