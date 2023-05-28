import json
import flet as ft

from pathlib import Path
from typing import List, Dict, Optional

data_path = Path("data")
data_path.mkdir(exist_ok=True)
genshin_path = data_path / "genshin.json"
starrail_path = data_path / "starrail.json"


class Base:
    character: List[str]
    type: List[str]


class Genshin(Base):
    character = [
        '旅行者',
        '神里绫华',
        '丽莎',
        '芭芭拉',
        '凯亚',
        '迪卢克',
        '雷泽',
        '安柏',
        '温迪',
        '香菱',
        '北斗',
        '行秋',
        '魈',
        '凝光',
        '可莉',
        '钟离',
        '菲谢尔',
        '班尼特',
        '达达利亚',
        '诺艾尔',
        '七七',
        '重云',
        '甘雨',
        '阿贝多',
        '迪奥娜',
        '莫娜',
        '刻晴',
        '砂糖',
        '辛焱',
        '罗莎莉亚',
        '胡桃',
        '枫原万叶',
        '烟绯',
        '宵宫',
        '托马',
        '优菈',
        '雷电将军',
        '早柚',
        '珊瑚宫心海',
        '五郎',
        '九条裟罗',
        '荒泷一斗',
        '八重神子',
        '鹿野院平藏',
        '夜兰',
        '埃洛伊',
        '申鹤',
        '云堇',
        '久岐忍',
        '神里绫人',
        '柯莱',
        '多莉',
        '提纳里',
        '妮露',
        '赛诺',
        '坎蒂丝',
        '纳西妲',
        '莱依拉',
        '流浪者',
        '珐露珊',
        '瑶瑶',
        '艾尔海森',
        '迪希雅',
        '米卡',
        '卡维',
        '白术',
    ]
    type = [
        '基础血量',
        '基础攻击力',
        '基础防御力',
        '攻击力',
        '攻击力百分比',
        '生命值',
        '生命值百分比',
        '防御力',
        '防御力百分比',
        '元素精通',
        '暴击率',
        '暴击伤害',
        '元素充能效率',
        '火元素抗性',
        '雷元素抗性',
        '冰元素抗性',
        '水元素抗性',
        '风元素抗性',
        '岩元素抗性',
        '草元素抗性',
        '火元素伤害加成',
        '雷元素伤害加成',
        '冰元素伤害加成',
        '水元素伤害加成',
        '风元素伤害加成',
        '岩元素伤害加成',
        '草元素伤害加成',
        '物理伤害加成',
        '治疗加成',
    ]


class Starrail(Base):
    character = [
        '开拓者·毁灭',
        '开拓者·存护',
        '三月七',
        '丹恒',
        '姬子',
        '瓦尔特',
        '卡芙卡',
        '银狼',
        '阿兰',
        '艾丝妲',
        '黑塔',
        '布洛妮娅',
        '希儿',
        '希露瓦',
        '杰帕德',
        '娜塔莎',
        '佩拉',
        '克拉拉',
        '桑博',
        '虎克',
        '青雀',
        '停云',
        '罗刹',
        '景元',
        '素裳',
        '彦卿',
        '白露',
    ]
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


class Core:
    def __init__(self, path: Path, model: Base):
        self.path = path
        self.model = model
        self.data: Dict[str, List[str]] = {}
        self.get_data_from_file()

    def get_data_from_file(self):
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                self.data = json.load(f)

    def save_data_to_file(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def get_value(self, ch_name: str, type_name: str) -> bool:
        return type_name in self.data.get(ch_name, [])

    def change_value(self, ch_name: str, type_name: List[str]):
        if len(type_name):
            self.data[ch_name] = type_name
        else:
            if ch_name in self.data:
                del self.data[ch_name]
        self.save_data_to_file()


class Page(ft.Page):
    core: Core
    current_name: Optional[str] = None
