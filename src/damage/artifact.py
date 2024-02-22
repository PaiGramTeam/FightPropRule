import json
from typing import Dict, List

from .assets import assets, locale
from .models import Artifact as ArtifactModel, WeaponConfig


class Artifact:
    def __init__(self):
        artifacts: List[ArtifactModel] = []
        artifact_config_map: Dict[str, ArtifactModel] = {}
        for value in assets.artifact.values():
            if not value["config4"]:
                continue
            cn_name = locale[value["name_locale"]]
            config_key = ArtifactModel.get_config_name(value["name"])
            config = []
            for i in value["config4"]:
                temp = json.loads(i)
                temp["title"] = locale[temp["title"]]
                temp["parent"] = config_key
                config.append(WeaponConfig(**temp))
            artifact_ = ArtifactModel(**value, cn_name=cn_name, config=config)
            artifacts.append(artifact_)
            artifact_config_map[config_key] = artifact_
        self.artifacts = artifacts
        self.artifact_config_map = artifact_config_map

    def get_by_name(self, name: str) -> ArtifactModel:
        return self.artifact_config_map.get(name)


artifact = Artifact()
