import json
import flet as ft

from httpx import get
from pathlib import Path
from typing import List, Dict, Optional

genshin_path = Path("FightPropRule_genshin.json")
starrail_path = Path("FightPropRule_starrail.json")
genshin_avatars_path = Path("avatars_genshin.json")
starrail_avatars_path = Path("avatars_starrail.json")
genshin_api = "https://api.ambr.top/v2/chs/avatar"
starrail_api = "https://api.yatta.top/hsr/v2/cn/avatar"


class Base:
    character: List[str]
    type: List[str]

    def get_data_from_file(self, path: Path):
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                self.character = json.load(f)
        else:
            self.character = []

    def save_data_to_file(self, path: Path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.character, f, ensure_ascii=False, indent=4)

    def get_data_from_api(self, api: str, ignore_id_start: str = None):
        if ignore_id_start is None:
            ignore_id_start = "-1"
        res = get(api)
        if res.status_code == 200:
            data = res.json()
            self.character = list(
                {
                    i.get("name")
                    for i in data.get("data", {}).get("items", {}).values()
                    if not str(i.get("id", 0)).startswith(ignore_id_start)
                }
            )


class Genshin(Base):
    type = [
        "基础血量",
        "基础攻击力",
        "基础防御力",
        "攻击力",
        "攻击力百分比",
        "生命值",
        "生命值百分比",
        "防御力",
        "防御力百分比",
        "元素精通",
        "暴击率",
        "暴击伤害",
        "元素充能效率",
        "火元素抗性",
        "雷元素抗性",
        "冰元素抗性",
        "水元素抗性",
        "风元素抗性",
        "岩元素抗性",
        "草元素抗性",
        "火元素伤害加成",
        "雷元素伤害加成",
        "冰元素伤害加成",
        "水元素伤害加成",
        "风元素伤害加成",
        "岩元素伤害加成",
        "草元素伤害加成",
        "物理伤害加成",
        "治疗加成",
    ]

    def __init__(self):
        self.get_data_from_file(genshin_avatars_path)

    def refresh(self):
        self.get_data_from_api(genshin_api)
        self.save_data_to_file(genshin_avatars_path)


class Starrail(Base):
    type = [
        "攻击力百分比",
        "攻击力",
        "击破特攻",
        "暴击率百分比",
        "暴击伤害百分比",
        "防御力百分比",
        "防御力",
        "火属性伤害提高百分比",
        "生命值百分比",
        "生命值",
        "治疗量加成百分比",
        "冰属性伤害提高百分比",
        "虚数属性伤害提高百分比",
        "物理属性伤害提高百分比",
        "量子属性伤害提高百分比",
        "速度",
        "能量恢复效率百分比",
        "效果命中百分比",
        "效果抵抗百分比",
        "雷属性伤害提高百分比",
        "风属性伤害提高百分比",
    ]

    def __init__(self):
        self.get_data_from_file(starrail_avatars_path)

    def refresh(self):
        self.get_data_from_api(starrail_api, "800")
        self.character.extend(
            [
                "开拓者·毁灭",
                "开拓者·存护",
            ]
        )
        self.save_data_to_file(starrail_avatars_path)


class Core:
    def __init__(self, path: Path, model: Base):
        self.path = path
        self.model = model
        self.data: Dict[str, Dict[str, float]] = {}
        self.get_data_from_file()

    def get_data_from_file(self):
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                self.data = json.load(f)

    def save_data_to_file(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def get_value(self, ch_name: str, type_name: str) -> bool:
        return type_name in self.data.get(ch_name, {})

    def get_prop_value(self, ch_name: str, type_name: str) -> str:
        return str(self.data.get(ch_name, {}).get(type_name, "0.0"))

    def set_prop_value(self, ch_name: str, type_name: str, value: str):
        if ch_name not in self.data:
            self.data[ch_name] = {}
        self.data[ch_name][type_name] = float(value)

    def remove_prop_value(self, ch_name: str, type_name: str):
        if ch_name not in self.data:
            return
        if type_name not in self.data[ch_name]:
            return
        self.data[ch_name] = {
            k: v for k, v in self.data[ch_name].copy().items() if k != type_name
        }

    def save_value(self):
        self.data = {k: v for k, v in self.data.copy().items() if v}
        self.save_data_to_file()


class Page(ft.Page):
    core: Core
    current_name: Optional[str] = None
    current_prop_name: Optional[str] = None
