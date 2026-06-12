import flet as ft
from views.Home_view import Home_view
def main(page: ft.Page):
    # إعدادات الشاشة الأساسية لمنع التجمد
    page.title = "USSD Test App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    try:
        # محاولة استدعاء الصفحة التي قمنا بتعديلها

        
        # عرض الصفحة فوراً
        page.views.clear()
        page.views.append(Home_view(page))
        page.update()

    except Exception as e:
        # إذا كان هناك أي خطأ (في الـ imports أو الكود) سيظهر هنا فوراً على الشاشة
        page.controls.clear()
        page.add(
            ft.Container(
                padding=20,
                bgcolor=ft.Colors.RED_500,
                border_radius=10,
                content=ft.Column(
                    controls=[
                        ft.Text("⚠️ تم اكتشاف خطأ يمنع تشغيل التطبيق:", color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(str(e), color=ft.Colors.WHITE, size=14, selectable=True)
                    ]
                )
            )
        )
        page.update()

ft.app(target=main)
