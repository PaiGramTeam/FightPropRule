from typing import List

from flet_core import MainAxisAlignment

import flet as ft

from src.data import Page
from .artifact import artifact
from .character import character
from .data import data
from .models import (
    CharacterSkill,
    CharacterDamageSkillDamageKey,
    CharacterConfig,
    Weapon as WeaponModel,
)
from .weapon import weapon


def edit_damage_view(page: "Page"):
    name_list = ft.ListView(width=230)
    skill_list = ft.ListView(expand=True)
    weapon_list = ft.ListView(expand=True)
    artifact_list = ft.ListView(expand=True)
    character_control_list = ft.ListView(expand=True)
    top_title = ft.Ref[ft.Text]()

    def update_top_title(title: str):
        """更新当前页面标题"""
        top_title.current.value = title
        page.update()

    def back_choose(_):
        page.go("/")
        page.update()

    def save(_):
        def close_alert(_):
            success_dialog.open = False
            top_title.current.value = ""
            choose_character()
            page.update()

        data.save()
        success_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("保存成功"),
            content=ft.Text("保存成功"),
            actions=[
                ft.TextButton("好", on_click=close_alert),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        page.dialog = success_dialog
        success_dialog.open = True
        page.update()

    def update_skill_component():
        ch_name = character.current_name
        skill_list.controls.clear()
        skill_list.controls.append(
            ft.Container(
                content=ft.Text(
                    "  技能配置",
                    size=20,
                ),
            )
        )
        for i in character.skills_map[ch_name]:
            container = ft.Container(
                content=ft.Checkbox(
                    label=i.show_name,
                    value=data.get_skill_value(ch_name, i),
                    disabled=True,
                    data=i,
                ),
                on_click=choose_skill,
            )
            skill_list.controls.append(container)

    def update_weapon_component():
        ch_name = character.current_name
        character_ = character.characters_map[ch_name]
        weapon_list.controls.clear()
        weapon_list.controls.append(
            ft.Container(
                content=ft.Text(
                    "  武器配置",
                    size=20,
                ),
            )
        )
        for i in weapon.weapon_map.get(character_.get("weapon", ""), []):
            i: "WeaponModel"
            container = ft.Container(
                content=ft.Checkbox(
                    label=i.cn_name,
                    value=data.get_weapon_config_enable(ch_name, i.name),
                    disabled=True,
                    data=i,
                ),
                on_click=choose_weapon,
            )
            weapon_list.controls.append(container)

    def update_artifact_component():
        ch_name = character.current_name
        artifact_list.controls.clear()
        artifact_list.controls.append(
            ft.Container(
                content=ft.Text(
                    "  圣遗物配置",
                    size=20,
                ),
            )
        )
        for i in artifact.artifacts:
            container = ft.Container(
                content=ft.Checkbox(
                    label=i.cn_name,
                    value=data.get_artifact_config_enable(ch_name, i.config_name),
                    disabled=True,
                    data=i,
                ),
                on_click=choose_artifact,
            )
            artifact_list.controls.append(container)

    def gen_switch_or_text(
        ch_name, config: CharacterConfig, get_config_value, on_change
    ):
        if isinstance(config.default, bool):
            class_ = ft.Checkbox
        else:
            class_ = ft.TextField
        return class_(
            label=config.title,
            value=get_config_value(ch_name, config),
            data=config,
            on_change=on_change,
        )

    def update_config_component(
        com: List,
        name: str,
        config_map,
        set_character_config_value,
        get_character_config_value,
    ):
        ch_name = character.current_name
        if not character.config_map[ch_name]:
            return
        com.append(
            ft.Container(
                content=ft.Text(
                    name,
                    size=20,
                ),
            ),
        )

        def on_config_value_change(e: ft.ControlEvent = None):
            set_character_config_value(ch_name, e.control.data, e.data)

        def reset_all_config_value(_):
            for config in configs:
                config.value = config.data.default
                set_character_config_value(ch_name, config.data, config.data.default)
            page.update()

        configs = []
        for i in config_map[ch_name]:
            content = gen_switch_or_text(
                ch_name, i, get_character_config_value, on_config_value_change
            )
            configs.append(content)
            com.append(
                ft.Container(
                    content=content,
                ),
            )
        if len(configs) != 0:
            com.append(
                ft.Container(
                    content=ft.ElevatedButton(
                        "恢复到默认值", on_click=reset_all_config_value
                    ),
                )
            )
        return com

    def choose_character(e: ft.ControlEvent = None):
        if e is not None:
            ch_name = e.control.data[0]
            character.current_name = ch_name
        else:
            ch_name = character.current_name
        page.update()
        update_top_title(ch_name)
        update_skill_component()
        update_weapon_component()
        update_artifact_component()
        character_control_list.controls.clear()
        com = []
        character_control_list.controls.append(ft.Column(com))
        update_config_component(
            com,
            "  角色配置",
            character.config_map,
            data.set_character_config_value,
            data.get_character_config_value,
        )
        update_config_component(
            com,
            "  技能配置",
            character.config_skill_map,
            data.set_character_skill_config_value,
            data.get_character_skill_config_value,
        )
        page.update()

    def bs_dismissed(_: ft.ControlEvent = None):
        choose_character()

    def choose_skill(e: ft.ControlEvent = None):
        checkbox: ft.Checkbox = e.control.content
        skill: CharacterSkill = checkbox.data
        page.overlay.clear()

        def close_bs(_: ft.ControlEvent = None):
            bs.open = False
            bs.update()

        def skill_status_change(e_: ft.ControlEvent = None):
            value = e_.data == "true"
            data.set_skill_value(character.current_name, skill, value)

        def skill_custom_name_change(e_: ft.ControlEvent = None):
            skill.custom_name = e_.data
            data.set_skill_value(character.current_name, skill, True)

        def skill_key_change(e_: ft.ControlEvent = None):
            skill.damage_key = CharacterDamageSkillDamageKey(e_.data)
            data.set_skill_value(character.current_name, skill, True)

        bs = ft.BottomSheet(
            ft.Container(
                ft.Column(
                    [
                        ft.Text(skill.show_name),
                        ft.Switch(
                            label="显示此数值",
                            value=checkbox.value,
                            on_change=skill_status_change,
                        ),
                        ft.TextField(
                            label="自定义显示名称",
                            value=skill.custom_name or skill.show_name,
                            on_change=skill_custom_name_change,
                        ),
                        ft.Dropdown(
                            label="输出数据",
                            options=[
                                ft.dropdown.Option(key=v, text=k)
                                for k, v in CharacterDamageSkillDamageKey.normal.data_map.items()
                            ],
                            value=skill.damage_key.value,
                            on_change=skill_key_change,
                        ),
                        ft.ElevatedButton("关闭", on_click=close_bs),
                    ],
                    tight=True,
                ),
                padding=10,
            ),
            open=True,
            on_dismiss=bs_dismissed,
        )
        page.overlay.append(bs)
        page.update()
        bs.update()

    def choose_weapon(e):
        choose_weapon_or_artifact(
            e,
            data.get_character_weapon_config_value,
            data.set_character_weapon_config_value,
        )

    def choose_artifact(e):
        choose_weapon_or_artifact(
            e,
            data.get_character_artifact_config_value,
            data.set_character_artifact_config_value,
        )

    def choose_weapon_or_artifact(
        e: ft.ControlEvent,
        get_config_value,
        set_config_value,
    ):
        ch_name = character.current_name
        checkbox: ft.Checkbox = e.control.content
        model: "WeaponModel" = checkbox.data
        page.overlay.clear()

        def close_bs(_: ft.ControlEvent = None):
            bs.open = False
            bs.update()

        def on_config_value_change(e_: ft.ControlEvent = None):
            set_config_value(ch_name, e_.control.data, e_.data)

        def reset_all_config_value(_):
            for config in configs:
                config.value = config.data.default
                set_config_value(ch_name, config.data, config.data.default)
            page.update()

        controls = [
            ft.Text(model.cn_name),
        ]
        configs = []
        for i in model.config:
            content = gen_switch_or_text(
                ch_name, i, get_config_value, on_config_value_change
            )
            configs.append(content)
            controls.append(content)
        controls.append(
            ft.Container(
                content=ft.ElevatedButton("恢复到默认值", on_click=reset_all_config_value),
            )
        )
        controls.append(ft.ElevatedButton("关闭", on_click=close_bs))

        bs = ft.BottomSheet(
            ft.Container(
                ft.Column(
                    controls,
                    tight=True,
                ),
                padding=10,
            ),
            open=True,
            on_dismiss=bs_dismissed,
        )
        page.overlay.append(bs)
        page.update()
        bs.update()

    def load_names():
        for index, name in enumerate(character.characters_name):
            name_list.controls.append(
                ft.TextButton(
                    text=name,
                    tooltip=name,
                    style=ft.ButtonStyle(
                        shape={
                            "hovered": ft.RoundedRectangleBorder(),
                            "": ft.RoundedRectangleBorder(),
                        }
                    ),
                    data=(name,),
                    on_click=choose_character,
                    disabled=False,
                ),
            )

    load_names()
    page.views.append(
        ft.View(
            "/edit_damage",
            [
                ft.Stack(
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Text(
                                        ref=top_title,
                                        value="请选择需要编辑的角色",
                                        size=30,
                                    ),
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "返回",
                                                icon=ft.icons.ARROW_BACK,
                                                on_click=back_choose,
                                            ),
                                            ft.ElevatedButton(
                                                "保存",
                                                icon=ft.icons.DONE,
                                                on_click=save,
                                            ),
                                        ],
                                        alignment=MainAxisAlignment.CENTER,
                                        spacing=50,
                                    ),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            padding=10,
                        ),
                    ]
                ),
                ft.Divider(
                    height=1,
                ),
                ft.Row(
                    [
                        name_list,
                        ft.VerticalDivider(width=1),
                        skill_list,
                        ft.VerticalDivider(width=1),
                        weapon_list,
                        ft.VerticalDivider(width=1),
                        artifact_list,
                        ft.VerticalDivider(width=1),
                        character_control_list,
                    ],
                    expand=True,
                    spacing=0,
                ),
            ],
            padding=0,
            spacing=0,
        )
    )
