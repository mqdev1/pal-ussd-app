import flet as ft

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.routes = {}
        # ربط حدث تغيير المسار بدالة المعالجة
        self.page.on_route_change = self._handle_route_change

    def register_route(self, route_name: str, view_factory):
        """تسجيل الواجهة كـ Function وليس كـ Object لحفظ الذاكرة"""
        self.routes[route_name] = view_factory

    def go_to(self, route_name: str):
        """الانتقال لمسار جديد وتحديث الـ URL/Route الخاص بـ Flet"""
        self.page.route = route_name
        self.page.update()

    def _handle_route_change(self, e):
        """المعالج الرئيسي الذي يبني الصفحة فقط عند زيارتها"""
        route_name = self.page.route
        if route_name in self.routes:
            # تنظيف الواجهات السابقة (أو يمكنك تركها لإدارة الـ Back Button)
            self.page.views.clear() 
            
            # بناء الصفحة الآن فقط في الذاكرة!
            view_control = self.routes[route_name]() 
            
            self.page.views.append(
                ft.View(
                    route=route_name,
                    padding=0,
                    spacing=0,
                    controls=[view_control],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO
                )
            )
            self.page.update()