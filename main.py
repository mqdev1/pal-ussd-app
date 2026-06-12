import flet as ft
from views.Home_view import Home_view

def main(page: ft.Page):
    page.title = "USSD Test App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # دالة الانتقال لصفحتك عند النقر على الزر
    def go_to_home(e):
        try:
            page.views.clear()
            # استدعاء صفحتك الأساسية ودفعها للـ Views
            page.views.append(Home_view(page))
            page.update()
        except Exception as error:
            # إذا انهار التطبيق داخل Home_view سيطبع لك السبب هنا باللون الأصفر فوراً
            page.add(
                ft.Container(
                    padding=15,
                    bgcolor=ft.Colors.AMBER_900,
                    content=ft.Text(f"خطأ داخل كود Home_view:\n{str(error)}", color=ft.Colors.WHITE)
                )
            )
            page.update()

    # شاشة البداية المؤقتة التي تحتوي على زرك المفسر
    page.controls.clear()
    page.add(
        ft.Container(
            alignment=ft.alignment.center,
            padding=30,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(name=ft.Icons.PHONELINK_SETUP, size=50, color=ft.Colors.BLUE),
                    ft.Text("مرحباً بك في تطبيق الفحص", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("اضغط على الزر أدناه لتشغيل الواجهة الرئيسية والتأكد من الـ Imports", size=14, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                    ft.VerticalDivider(height=20),
                    # الزر الذي اقترحته أنت
                    ft.ElevatedButton(
                        text="دخول إلى الواجهة الرئيسية 🚀",
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE,
                        on_click=go_to_home,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    )
                ]
            )
        )
    )
    page.update()

ft.app(target=main)
