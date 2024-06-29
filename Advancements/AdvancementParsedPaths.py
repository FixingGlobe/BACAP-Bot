import os
from typing import Optional
import re


class AdvancementParsedPaths:
    def __init__(self, advancement_path: str):
        parts = advancement_path.split(os.sep)  # Разбиваем путь на части
        parts[2] = 'bc_rewards'  # Заменяем "bacaped" или "blazeandcave" на bc_rewards
        parts[3] = 'function'  # Заменяем "advancements" на "functions"
        parts[-1] = parts[-1].replace('.json', '.mcfunction')  # Заменяем расширение файла на .mcfunction

        base_parts = parts[:4] + parts[4:]  # Базовые части пути без вставок

        # Создаем новые пути для каждого типа
        reward_path = os.sep.join(base_parts[:4] + ['reward'] + base_parts[4:])
        experience_path = os.sep.join(base_parts[:4] + ['exp'] + base_parts[4:])
        trophy_path = os.sep.join(base_parts[:4] + ['trophy'] + base_parts[4:])
        message_path = os.sep.join(base_parts[:4] + ['msg'] + base_parts[4:])

        self._advancement = advancement_path
        self._message = message_path if os.path.exists(message_path) and not self.__is_file_empty(message_path) else None
        self._experience = experience_path if os.path.exists(experience_path) and not self.__is_file_empty(experience_path) else None
        self._reward = reward_path if os.path.exists(reward_path) and not self.__is_file_empty(reward_path) else None
        self._trophy = trophy_path if os.path.exists(trophy_path) and not self.__is_file_empty(trophy_path) else None

    @property
    def advancement(self) -> str:
        return self._advancement

    @property
    def message(self) -> Optional[str]:
        return self._message

    @property
    def experience(self) -> Optional[str]:
        return self._experience

    @property
    def reward(self) -> Optional[str]:
        return self._reward

    @property
    def trophy(self) -> Optional[str]:
        return self._trophy

    @staticmethod
    def __is_file_empty(file_path: str) -> bool:
        with open(file_path, encoding='UTF-8') as file:
            content = file.read().strip()
            return not content

    @staticmethod
    def minecraft_parent_to_file_path(minecraft_path: str) -> Optional[str]:
        """
        Converts an internal Minecraft file path to the actual advancement path.

        :param minecraft_path: Internal Minecraft file path, e.g., blazeandcave:bacap/challenges_milestone
        :return: Actual advancement path, e.g., bacap\\data\\blazeandcave\\advancement\\bacap\\challenges_milestone.json,
                 or None if the path was not found.
        """
        if not minecraft_path:
            return None

        # Разделяем путь по символам ':' и '/'
        splitted_path = re.split('[:/]', minecraft_path)

        # Проверяем, что путь содержит все необходимые части
        if len(splitted_path) != 3:
            return None

        # Пространства имён
        namespaces = {"blazeandcave": "bacap", "minecraft": "bacap", "bacaped": "bacaped"}
        namespace = namespaces.get(splitted_path[0])

        if not namespace:
            return None

        # Формируем новый путь
        actual_path = os.path.join(namespace, "data", splitted_path[0], "advancement", splitted_path[1], f"{splitted_path[2]}.json")

        if os.path.exists(actual_path):
            return actual_path
        return None


if __name__ == '__main__':
    print(AdvancementParsedPaths.minecraft_parent_to_file_path("bacaped:adventure/advancement_info"))
