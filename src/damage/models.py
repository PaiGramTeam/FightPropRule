from enum import Enum
from typing import List, Dict, Any, Optional

from pydantic import BaseModel


class CharacterDamageSkillDamageKey(str, Enum):
    normal = "normal"
    """普通伤害结果"""
    melt = "melt"
    """融化伤害结果"""
    vaporize = "vaporize"
    """蒸发伤害结果"""

    @property
    def data_map(self) -> Dict[str, str]:
        return {"普通伤害结果": "normal", "融化伤害结果": "melt", "蒸发伤害结果": "vaporize"}


class CharacterDamageSkill(BaseModel):
    name: str
    index: int
    damage_key: CharacterDamageSkillDamageKey

    class Config:
        frozen = False


class CharacterDamage(BaseModel):
    skills: List[CharacterDamageSkill]
    config: Optional[Dict[str, Any]] = None
    config_skill: Optional[Dict[str, Any]] = None
    config_weapon: Optional[Dict[str, Dict[str, Any]]] = None
    artifact_config: Optional[Dict[str, Dict[str, Any]]] = None

    class Config:
        frozen = False


class CharacterConfig(BaseModel):
    default: Any
    name: str
    title: str

    class Config:
        frozen = False


class CharacterSkill(BaseModel):
    name: str
    index: int
    skill_name: str
    custom_name: str = ""
    damage_key: CharacterDamageSkillDamageKey = CharacterDamageSkillDamageKey.normal

    @property
    def show_name(self) -> str:
        return f"{self.name} - {self.skill_name}"

    def to_data(self) -> CharacterDamageSkill:
        return CharacterDamageSkill(
            name=self.custom_name or self.show_name,
            index=self.index,
            damage_key=self.damage_key,
        )

    class Config:
        frozen = False


class WeaponConfig(CharacterConfig):
    max: float = 0
    min: float = 0
    parent: str = ""

    class Config:
        frozen = False


class Weapon(BaseModel):
    name: str
    cn_name: str
    star: int
    t: str
    config: List[WeaponConfig]

    class Config:
        frozen = False


class Artifact(BaseModel):
    name: str
    cn_name: str
    min_star: int
    max_star: int
    config: List[WeaponConfig]

    @property
    def config_name(self) -> str:
        return self.get_config_name(self.name)

    @staticmethod
    def get_config_name(name: str) -> str:
        start = "config_"
        # 将大写转换为下划线加小写
        # 例如: MaxHp -> max_hp
        convert_name = "".join(
            [f"_{i.lower()}" if i.isupper() else i for i in name]
        ).lstrip("_")
        return f"{start}{convert_name}"

    class Config:
        frozen = False
