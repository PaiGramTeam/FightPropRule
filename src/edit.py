from flet_core import MainAxisAlignment

from src.components import show_snack_bar

import flet as ft

from src.data import Page


def edit_view(page: Page):
    page.current_name = ""
    name_list = ft.ListView(
        width=230,
    )
    prop_list = ft.ListView(
        expand=True,
    )
    top_title = ft.Ref[ft.Text]()

    def update_top_title(title: str):
        """更新当前页面标题"""
        top_title.current.value = title
        page.update()

    def back_choose(_):
        page.go("/")
        page.update()

    def choose_character(e=None):
        if e is not None:
            ch_name = e.control.data[0]
            page.current_name = ch_name
        else:
            ch_name = page.current_name
        # 获取课程任务列表
        page.update()
        update_top_title(ch_name)
        prop_list.controls.clear()
        for i in page.core.model.type:
            prop_list.controls.append(
                ft.Checkbox(
                    label=i,
                    value=page.core.get_value(ch_name, i),
                    disabled=False,
                    data=i,
                )
            )
        page.update()

    for index, name in enumerate(page.core.model.character):
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
                data=(
                    name,
                ),
                on_click=choose_character,
                disabled=False,
            ),
        )

    def save(_):
        choose_results = list(
            filter(
                lambda x: x is not None,
                map(
                    lambda x: x.data if x.value else None,
                    prop_list.controls.copy(),
                ),
            )
        )

        if len(choose_results) == 0:
            show_snack_bar(page, "已清空有效词条〜", ft.colors.ERROR)

        def close_alert(_):
            success_dialog.open = False
            top_title.current.value = ""
            choose_character()
            page.update()

        page.core.change_value(page.current_name, choose_results)
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

    def select_all(_):
        prop_list_controls = prop_list.controls.copy()
        have_selection_some = len(
            list(filter(lambda prop_: prop_.value, prop_list_controls))
        ) < len(prop_list_controls)

        if have_selection_some:
            for prop in prop_list_controls:
                prop.value = True
        else:
            for i in prop_list_controls:
                i.value = not i.value if i.disabled is False else i.value
        page.update()

    page.views.append(
        ft.View(
            "/edit",
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
                                                "全选",
                                                icon=ft.icons.ALL_INBOX,
                                                on_click=select_all,
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
                    [name_list, ft.VerticalDivider(width=1), prop_list],
                    expand=True,
                    spacing=0,
                ),
            ],
            padding=0,
            spacing=0,
        )
    )
