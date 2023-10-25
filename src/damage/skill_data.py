import flet as ft
from typing import Dict, List, Optional

from src.damage.character import character
from src.damage.models import (
    CharacterDamage,
    CharacterDamageSkill,
    CharacterSkill,
    CharacterDamageSkillDamageKey,
    CharacterDamageSkillTransformativeDamageKey,
)


class SkillData:
    def __init__(self, file_data: Dict[str, CharacterDamage]):
        self.file_data = file_data
        self.temp: Optional[CharacterDamageSkill] = None
        self.temp_index: Dict[int, CharacterSkill] = {}

    def get(self, character_name: str) -> List[CharacterDamageSkill]:
        if character_name not in self.file_data:
            return []
        return self.file_data[character_name].skills

    def delete_skill(self):
        if self.temp and self.temp in self.file_data[character.current_name].skills:
            self.file_data[character.current_name].skills.remove(self.temp)
            self.temp = None
            self.temp_index.clear()

    @staticmethod
    def get_skill_show_name(character_name: str, skill: CharacterDamageSkill) -> str:
        for i in character.skills_map[character_name]:
            if i.index == skill.index:
                return i.show_name
        return skill.name

    @staticmethod
    def get_dropdown_options(character_name: str) -> List[ft.dropdown.Option]:
        skills = []
        for skill in character.skills_map[character_name]:
            skills.append(
                ft.dropdown.Option(
                    key=skill.index,
                    text=skill.show_name,
                )
            )
        return skills

    def init_temp_index(self, character_name: str):
        self.temp_index.clear()
        for skill in character.skills_map[character_name]:
            self.temp_index[skill.index] = skill

    def create_first(self, character_name: str):
        self.temp = CharacterDamageSkill(name="", index=-1)
        self.init_temp_index(character_name)

    def create_handle_index(self, e: ft.ControlEvent = None):
        index = int(e.data)
        self.temp.index = index
        self.temp.name = self.temp_index[index].show_name

    def create_handle_name(self, e: ft.ControlEvent = None):
        if e.data == "":
            self.temp.name = self.temp_index[self.temp.index].show_name
        else:
            self.temp.name = e.data

    def create_handle_damage_key(self, e: ft.ControlEvent = None):
        self.temp.damage_key = CharacterDamageSkillDamageKey(e.data)
        self.temp.transformative_damage_key = None

    def create_handle_transformative_damage_key(self, e: ft.ControlEvent = None):
        self.temp.transformative_damage_key = (
            CharacterDamageSkillTransformativeDamageKey(e.data)
        )
        self.temp.damage_key = None

    def create_confirm(self) -> bool:
        if self.temp.index == -1:
            return False
        if not self.temp.damage_key and not self.temp.transformative_damage_key:
            return False
        if not self.file_data.get(character.current_name):
            self.file_data[character.current_name] = CharacterDamage(skills=[])
        self.file_data[character.current_name].skills.append(self.temp)
        self.temp = None
        self.temp_index.clear()
        return True
