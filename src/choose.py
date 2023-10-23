from flet_core import MainAxisAlignment, CrossAxisAlignment

from src.components import show_snack_bar

import flet as ft

from src.data import Core, genshin_path, Genshin, starrail_path, Starrail, Page


def choose_view(page: Page):
    def genshin(_e):
        page.core = Core(genshin_path, Genshin())
        page.go("/edit")
        show_snack_bar(page, "开始编辑原神圣遗物有效词条", ft.colors.GREEN)

    def genshin_damage(_e):
        page.go("/edit_damage")
        show_snack_bar(page, "开始编辑原神伤害计算规则", ft.colors.GREEN)

    def starrail(_e):
        page.core = Core(starrail_path, Starrail())
        page.go("/edit")
        show_snack_bar(page, "开始编辑崩坏：星穹铁道遗器有效词条", ft.colors.GREEN)

    def refresh(_e):
        Genshin().refresh()
        Starrail().refresh()
        show_snack_bar(page, "刷新角色列表成功", ft.colors.GREEN)

    # View
    page.views.append(
        ft.View(
            "/",
            [
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(
                                "GramBotMetadataEditor",
                                size=50,
                            ),
                        ),
                        ft.FilledButton(
                            "Genshin",
                            icon=ft.icons.LOGIN,
                            on_click=genshin,
                        ),
                        ft.FilledButton(
                            "Starrail",
                            icon=ft.icons.LOGIN,
                            on_click=starrail,
                        ),
                        ft.FilledButton(
                            "GenshinDamage",
                            icon=ft.icons.LOGIN,
                            on_click=genshin_damage,
                        ),
                        ft.FilledButton(
                            "Refresh avatars",
                            icon=ft.icons.LOGIN,
                            on_click=refresh,
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                )
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
        )
    )
