import flet as ft
from views.Home_view import Home_view  # تأكد من المسار الصحيح للملف

def main(page: ft.Page):
    # إعدادات الصفحة الأساسية
    page.title = "USSD Jawwal"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # دالة إدارة التنقل بين الصفحات (Routing)
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            # استدعاء الدالة التي عدلناها معاً
            page.views.append(Home_view(page))
        page.update()

    page.on_route_change = route_change
    page.go("/") # التوجه فوراً لصفحة البداية

ft.app(target=main)
