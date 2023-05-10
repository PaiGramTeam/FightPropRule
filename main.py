import flet as ft

from src.choose import choose_view
from src.data import Page
from src.edit import edit_view


def main(page: Page):
    def on_route_change(e: Page):
        page.views.clear()
        choose_view(page)
        if e.route == "/edit":
            edit_view(page)
        page.update()

    def view_pop():
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.title = "PropScoreEditor"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.on_route_change = on_route_change
    page.on_view_pop = view_pop
    page.window_min_width = 800
    page.window_width = 800
    page.window_height = 600
    page.window_min_height = 600
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)
