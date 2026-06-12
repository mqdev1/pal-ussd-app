import flet as ft
from views.Home_view import Home_view

def main(page: ft.Page):
    page.title = "USSD Jawwal Pay"
    page.theme_mode = ft.ThemeMode.LIGHT

    # معالج التغيير للمسارات (Route Change) بدون الـ Loop اللاهوائي
    def route_change(e):
        troute = ft.TemplateRoute(page.route)
        
        # لا نقم بعمل clear للـ views إلا إذا تأكدنا من المطابقة
        if troute.match("/"):
            page.views.clear()
            page.views.append(Home_view(page))
            
        page.update()

    def view_pop(view):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            page.window_close()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # الانطلاق الآمن
    page.go("/")

ft.app(target=main)
