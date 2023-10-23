import json
from typing import Dict

from .assets import assets, locale
from .models import Weapon as WeaponModel, WeaponConfig


class Weapon:
    def __init__(self):
        weapon_map: Dict[str, WeaponModel] = {}
        for value in assets.weapon.values():
            if not value["configs"]:
                continue
            cn_name = locale[value["name_index"]]
            config = []
            for i in value["configs"]:
                temp = json.loads(i)
                temp["title"] = locale[temp["title"]]
                temp["parent"] = value["name"]
                config.append(WeaponConfig(**temp))
            weapon_ = WeaponModel(**value, cn_name=cn_name, config=config)
            temp = weapon_map.get(value["t"], [])
            temp.append(weapon_)
            weapon_map[value["t"]] = temp
        self.weapon_map = weapon_map


weapon = Weapon()
