import flet as ft
# استيراد واجهتك الأصلية

def main(page: ft.Page):
    # 1. إعدادات الشاشة الأساسية والتصميم النظيف
    page.title = "USSD Direct Test"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0  # تصفير الحواف لملء الشاشة بالكامل مثل الـ Vie
      # حماية شاملة: إذا كان هناك أي سطر أو مكتبة تسبب كراش داخل Home_view ستظهر هنا باللون البرتقالي
    page.controls.clear()
    page.add(
            ft.Container(
                padding=20,
                margin=20,
                bgcolor=ft.Colors.ORANGE_900,
                border_radius=10,
                alignment=ft.alignment.center,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(name=ft.Icons.BUG_REPORT, size=40, color=ft.Colors.WHITE),
                        ft.Text("⚠️ تم رصد مشكلة داخل كود الواجهة:", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(str(e), color=ft.Colors.WHITE, size=13, selectable=True)
                    ]
                )
            )
        )
    page.update()

ft.app(target=main)
