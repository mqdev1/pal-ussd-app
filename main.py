
import flet as ft

from views.Home_view import Home_view

def main(page:ft.Page):


    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 400
    page.window.height = 700

    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(e: ft.RouteChangeEvent):

        page.views.clear()
        

        page.views.append(Home_view(page))
        

        page.update()

    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    page.go(page.route)

        

if __name__ == '__main__':
    ft.app(target=main,assets_dir="assets")