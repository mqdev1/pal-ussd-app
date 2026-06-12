import flet as ft

def main(page: ft.Page):
    # إعدادات الشاشة الأساسية لمنع التجمد
    page.title = "USSD Test App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.controls.clear()
    page.add(
            ft.Container(
                padding=20,
                bgcolor=ft.Colors.RED_500,
                border_radius=10,
                content=ft.Column(
                    controls=[
                        ft.Text("⚠️ تم اكتشاف خطأ يمنع تشغيل التطبيق:", color=ft.Colors.GREY, size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("Mahmoud qasem", color=ft.Colors.GREY, size=14, selectable=True)
                    ]
                )
            )
        )
    page.update()

ft.app(target=main)
