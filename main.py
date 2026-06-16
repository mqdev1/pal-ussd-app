import flet as ft
from views.test_view import test_view

def main(page: ft.Page):
    page.title = "Flet Routing App"

    # 1. تعريف القاموس باستخدام lambda لإرجاع كائن الـ View عند الحاجة فقط
    # تأكد أن دالة test_view في ملفك الخارجي ترجع كائن ft.View مباشرة
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
        "/test": lambda: test_view(page=page) 
    }

    # 2. معالجة تغيير الروت بناءً على التكديس التراكمي
    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        
        # دائماً نضع الـ Home كقاعدة للتطبيق في الأسفل
        page.views.append(views["/"]()) # لاحظ الأقواس () لتشغيل الـ lambda
        
        # إذا كان الروت ليس الرئيسية، نقوم بتكديس الصفحة المطلوبة فوق الرئيسية
        if page.route != "/":
            if page.route in views:
                page.views.append(views[page.route]())
            else:
                # صفحة 404 اختيارية في حال كتابة روت خاطئ
                page.views.append(ft.View(route="/404", controls=[ft.Text("Page not found!")]))
            
        page.update()

    # 3. معالجة زر الرجوع (Back Button)
    def view_pop(e: ft.ViewPopEvent):
        if len(page.views) > 1:
            page.views.pop() # حذف الصفحة العلوية
            top_view = page.views[-1] # الحصول على الصفحة السابقة
            page.route = top_view.route # تحديث المسار نصياً
            page.update()

    # 4. تعيين الأحداث
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # 5. إطلاق التطبيق
    page.go(page.route)

ft.app(target=main)
