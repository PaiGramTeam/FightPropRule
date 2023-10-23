import json
from typing import List, Dict

from .assets import assets, locale
from .models import CharacterConfig, CharacterSkill


class Character:
    def __init__(self):
        self.current_name = ""
        self.characters_map = {}
        self.skills_map = {}
        self.config_map = {}
        self.config_skill_map = {}
        for value in assets.character.values():
            character_name = locale[value["name_locale"]]
            self.characters_map[character_name] = value
            self.skills_map[character_name] = self.gen_skills_model(value)
            self.config_map[character_name] = self.gen_config_model(value["config"])
            self.config_skill_map[character_name] = self.gen_config_model(
                value["config_skill"]
            )
        self.characters_name = list(self.characters_map.keys())

    @staticmethod
    def gen_skills_model(character_: Dict) -> List[CharacterSkill]:
        skills = []
        skill1_name = locale[character_.get("skill1_name_index")]
        skill2_name = locale[character_.get("skill2_name_index")]
        skill3_name = locale[character_.get("skill3_name_index")]
        for skill_name, skill in [
            (skill1_name, character_["skill_map1"]),
            (skill2_name, character_["skill_map2"]),
            (skill3_name, character_["skill_map3"]),
        ]:
            for i in skill:
                skills.append(
                    CharacterSkill(
                        name=locale[i["locale_index"]],
                        index=i["index"],
                        skill_name=skill_name,
                    )
                )
        return skills

    @staticmethod
    def gen_config_model(config: List[str]) -> List[CharacterConfig]:
        data = []
        for i in config:
            temp = json.loads(i)
            temp["title"] = locale[temp["title"]]
            data.append(CharacterConfig(**temp))
        return data


character = Character()
