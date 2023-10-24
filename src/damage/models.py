import flet
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

Element4OP = [
    flet.dropdown.Option(key="Cyro", text="冰元素"),
    flet.dropdown.Option(key="Electro", text="雷元素"),
    flet.dropdown.Option(key="Hydro", text="水元素"),
    flet.dropdown.Option(key="Pyro", text="火元素"),
]
Element8OP = Element4OP + [
    flet.dropdown.Option(key="Anemo", text="风元素"),
    flet.dropdown.Option(key="Dendro", text="草元素"),
    flet.dropdown.Option(key="Geo", text="岩元素"),
    flet.dropdown.Option(key="Physical", text="物理伤害"),
]


class Element4(str, Enum):
    Cyro = "Cyro"
    """冰元素"""
    Electro = "Electro"
    """雷元素"""
    Hydro = "Hydro"
    """水元素"""
    Pyro = "Pyro"
    """火元素"""


class Element8(str, Enum):
    Cyro = "Cyro"
    """冰元素"""
    Electro = "Electro"
    """雷元素"""
    Hydro = "Hydro"
    """水元素"""
    Pyro = "Pyro"
    """火元素"""
    Anemo = "Anemo"
    """风元素"""
    Dendro = "Dendro"
    """草元素"""
    Geo = "Geo"
    """岩元素"""
    Physical = "Physical"
    """物理伤害"""


class CharacterDamageSkillDamageKey(str, Enum):
    normal = "normal"
    """普通伤害结果"""
    melt = "melt"
    """融化伤害结果"""
    vaporize = "vaporize"
    """蒸发伤害结果"""
    spread = "spread"
    """蔓激化伤害结果"""
    aggravate = "aggravate"
    """超激化伤害结果"""

    @property
    def data_map(self) -> Dict[str, str]:
        return {
            "普通伤害结果": "normal",
            "融化伤害结果": "melt",
            "蒸发伤害结果": "vaporize",
            "蔓激化伤害结果": "spread",
            "超激化伤害结果": "aggravate",
        }


class CharacterDamageSkillTransformativeDamageKey(str, Enum):
    swirl_cryo = "swirl_cryo"
    swirl_hydro = "swirl_hydro"
    swirl_pyro = "swirl_pyro"
    swirl_electro = "swirl_electro"
    overload = "overload"
    electro_charged = "electro_charged"
    shatter = "shatter"
    super_conduct = "super_conduct"
    bloom = "bloom"
    hyper_bloom = "hyper_bloom"
    burgeon = "burgeon"
    burning = "burning"
    crystallize = "crystallize"

    @property
    def data_map(self) -> Dict[str, str]:
        return {
            "扩散（冰）伤害值": "swirl_cryo",
            "扩散（水）伤害值": "swirl_hydro",
            "扩散（火）伤害值": "swirl_pyro",
            "扩散（雷）伤害值": "swirl_electro",
            "超载伤害值": "overload",
            "感电伤害值": "electro_charged",
            "碎冰伤害值": "shatter",
            "超导伤害值": "super_conduct",
            "绽放伤害值": "bloom",
            "烈绽放伤害值": "hyper_bloom",
            "超绽放伤害值": "burgeon",
            "燃烧伤害值": "burning",
            "结晶盾伤害吸收量": "crystallize",
        }


class CharacterDamageSkill(BaseModel):
    name: str
    index: int
    damage_key: Optional[CharacterDamageSkillDamageKey] = None
    transformative_damage_key: Optional[
        CharacterDamageSkillTransformativeDamageKey
    ] = None

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
    type: str

    class Config:
        frozen = False


class CharacterSkill(BaseModel):
    name: str
    index: int
    skill_name: str
    custom_name: str = ""
    damage_key: Optional[CharacterDamageSkillDamageKey] = None
    transformative_damage_key: Optional[
        CharacterDamageSkillTransformativeDamageKey
    ] = None

    @property
    def show_name(self) -> str:
        return f"{self.name} - {self.skill_name}"

    def to_data(self) -> CharacterDamageSkill:
        return CharacterDamageSkill(
            name=self.custom_name or self.show_name,
            index=self.index,
            damage_key=self.damage_key,
            transformative_damage_key=self.transformative_damage_key,
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
