import flet as ft
from views.Home_view import Home_view

def main(page: ft.Page):
    # 1. إعدادات الشاشة الأساسية والتصميم
    page.title = "USSD App"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # 2. دالة معالجة التنقل بين الصفحات (Route Change Handler)
    def route_change(e):
        try:
            # تنظيف الـ views الحالية لمنع التراكم والتجميد
            page.views.clear()
            
            # المسار الرئيسي للتطبيق
            if page.route == "/":
                # استدعاء الـ View المصلح وتمرير الـ page له
                home_screen = Home_view(page)
                page.views.append(home_screen)
                
            page.update()
            
        except Exception as error:
            # إذا حدث خطأ داخل الـ Home_view أثناء التنقل، سيتم عرضه هنا فوراً
            page.views.clear()
            page.views.append(
                ft.View(
                    route="/error",
                    controls=[
                        ft.Container(
                            padding=20,
                            bgcolor=ft.Colors.RED_500,
                            border_radius=10,
                            content=ft.Column(
                                controls=[
                                    ft.Text("⚠️ خطأ في تحميل مسار الصفحة:", color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(str(error), color=ft.Colors.WHITE, size=14, selectable=True)
                                ]
                            )
                        )
                    ]
                )
            )
            page.update()

    # 3. ربط الدالة بحدث تغيير المسار في Flet
    page.on_route_change = route_change
    
    # 4. توجيه التطبيق فوراً عند الإقلاع للمسار الرئيسي "/" لتشغيل الدالة أعلاه
    page.go("/")

ft.app(target=main)
