import flet as ft
from views.Home_view import Home_view 

def main(page: ft.Page):
    page.title = "USSD PAL"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    try:
        def change_route(route_event):
            page.views.clear()
            
            # بناء واستدعاء الواجهة بأمان
            current_view = Home_view(page)
            page.views.append(current_view)
            page.update()

        def view_pop(view_event):
            if len(page.views) > 1:
                page.views.pop()
                top_view = page.views[-1]
                page.go(top_view.route)
            else:
                page.go('/')
            
        page.on_route_change = change_route
        page.on_view_pop = view_pop
        
        # التوجه للمسار الرئيسي لإقلاع المحرك
        page.go('/')
        
    except Exception as ex:
        page.views.clear()
        page.clean()
        
        page.add(
            ft.Container(
                alignment=ft.alignment.center,
                expand=True,
                bgcolor=ft.colors.GREY_50,
                padding=20,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Icon(name=ft.icons.ERROR_OUTLINE_ROUNDED, color=ft.colors.RED_400, size=80),
                        ft.Text("عذراً، حدث خطأ غير متوقع!", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_GREY_900),
                        ft.Container(
                            content=ft.Text(f"رمز الخطأ:\n{str(ex)}", size=12, color=ft.Colors.RED_800, font_family="monospace"),
                            bgcolor=ft.colors.RED_50, padding=15, border_radius=10
                        ),
                        ft.ElevatedButton(text="إعادة المحاولة", icon=ft.icons.REFRESH_ROUNDED, on_click=lambda _: page.go("/"))
                    ]
                )
            )
        )
        page.update()

# تشغيل التطبيق مع الحفاظ على مجلد الأصول
if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')
