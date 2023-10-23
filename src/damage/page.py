from typing import List

from flet_core import MainAxisAlignment

import flet as ft

from src.data import Page
from .character import character
from .data import data
from .models import CharacterSkill, CharacterDamageSkillDamageKey, CharacterConfig


def edit_damage_view(page: "Page"):
    name_list = ft.ListView(width=230)
    skill_list = ft.ListView(expand=True)
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

    def update_config_component() -> List:
        ch_name = character.current_name
        character_control_list.controls.clear()
        com = []
        character_control_list.controls.append(ft.Column(com))
        com.append(
            ft.Container(
                content=ft.Text(
                    "  角色配置",
                    size=20,
                ),
            ),
        )

        def on_config_value_change(e: ft.ControlEvent = None):
            data.set_character_config_value(ch_name, e.control.data, e.data)

        def gen_switch_or_text(config: CharacterConfig):
            if isinstance(config.default, bool):
                class_ = ft.Checkbox
            else:
                class_ = ft.TextField
            return class_(
                label=config.title,
                value=data.get_character_config_value(ch_name, config),
                data=config,
                on_change=on_config_value_change,
            )

        def reset_all_config_value(_):
            for config in configs:
                config.value = config.data.default
                data.set_character_config_value(ch_name, config.data, config.data.default)
            page.update()

        configs = []
        for i in character.config_map[ch_name]:
            content = gen_switch_or_text(i)
            configs.append(content)
            com.append(
                ft.Container(
                    content=content,
                ),
            )
        if len(configs) != 0:
            com.append(
                ft.Container(
                    content=ft.ElevatedButton("恢复到默认值", on_click=reset_all_config_value),
                )
            )

    def choose_character(e: ft.ControlEvent = None):
        if e is not None:
            ch_name = e.control.data[0]
            character.current_name = ch_name
        else:
            ch_name = character.current_name
        page.update()
        update_top_title(ch_name)
        update_skill_component()
        update_config_component()
        page.update()

    def choose_skill(e: ft.ControlEvent = None):
        checkbox: ft.Checkbox = e.control.content
        skill: CharacterSkill = checkbox.data
        page.overlay.clear()

        def bs_dismissed(_: ft.ControlEvent = None):
            choose_character()

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
