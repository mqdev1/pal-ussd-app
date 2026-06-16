
import flet as ft

def test_view(page: ft.Page):

    return ft.View(
        route='/test',
        controls=[
            ft.Text("This is test page"),
            ft.ElevatedButton(text="Go Back", on_click=lambda _:page.go('/'))
        ]
    )
