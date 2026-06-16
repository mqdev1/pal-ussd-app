import flet as ft
from views.test_view import test_view

def main(page: ft.Page):
    page.title = "Flet Routing App"

    # 1. تعريف القاموس
    views = {
        "/": lambda: ft.View(
            route="/",
            controls=[
                ft.AppBar(title=ft.Text("Home"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                ft.ElevatedButton("Go to Settings", on_click=lambda _: page.go("/settings")),
                ft.ElevatedButton("Go to Test", on_click=lambda _: page.go("/test")),
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        "/settings": lambda: ft.View(
            route="/settings",
            controls=[
                ft.AppBar(title=ft.Text("Settings"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
            ],
        ),
        # استدعاء الدالة الخارجية مع تمرير كائن الصفحة الحالي
        "/test": lambda: test_view(page) 
    }

    # 2. معالجة تغيير الروت بناءً على التكديس التراكمي
    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        
        # دائماً نضع الـ Home كقاعدة للتطبيق في الأسفل
        page.views.append(views["/"]()) 
        
        # التأكد من سلامة الروت الحالي
        current_route = page.route if page.route else "/"
        
        if current_route != "/":
            if current_route in views:
                try:
                    page.views.append(views[current_route]())
                except Exception as ex:
                    print(f"Error loading view: {ex}")
                    # في حال حدوث أي خطأ بالصفحة الخارجية لا يعلق التطبيق بل يظهر صفحة خطأ آمنة
                    page.views.append(ft.View(route="/error", controls=[ft.Text(f"Error: {ex}")]))
            else:
                page.views.append(ft.View(route="/404", controls=[ft.Text("Page not found!")]))
            
        page.update()

    # 3. معالجة زر الرجوع (Back Button)
    def view_pop(e: ft.ViewPopEvent):
        if len(page.views) > 1:
            page.views.pop() 
            top_view = page.views[-1] 
            page.route = top_view.route 
            page.update()

    # 4. تعيين الأحداث
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # 5. إطلاق التطبيق الآمن (التأكد من أن الروت الابتدائي صالح)
    initial_route = page.route if page.route in views else "/"
    page.go(initial_route)

ft.app(target=main)
