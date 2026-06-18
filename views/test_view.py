
import flet as ft
from Router import Router
def test_view(page:ft.Page, route:Router) -> ft.Control:
    return ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Page1", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY),
                ft.ElevatedButton(text="Back to home", on_click=lambda _:route.go_to("home_view"))
            ]
        )
