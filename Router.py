import flet as ft

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.routes = {}
        
        # ربط الأحداث بالدوال المحدثة في النسخ الجديدة
        self.page.on_route_change = self._handle_route_change
        self.page.on_view_pop = self._handle_view_pop

    def register_route(self, route_name: str, view_factory):
        """تسجيل الواجهة كـ Function لحفظ الذاكرة وعدم بنائها إلا عند الحاجة"""
        self.routes[route_name] = view_factory

    def go_to(self, route_name: str):
        """الانتقال لمسار جديد بالطريقة الحديثة المعتمدة في Flet"""
        self.page.go(route_name)

    def _handle_route_change(self, e: ft.RouteChangeEvent):
        """المعالج الرئيسي الذي يبني الصفحة بناءً على حدث تغيير المسار الجديد"""
        # قراءة المسار الجديد مباشرة من الحدث أو الصفحة
        route_name = e.route if e else self.page.route
        
        if route_name in self.routes:
            # تنظيف الواجهات السابقة لبناء الشاشة الجديدة
            self.page.views.clear() 
            
            # بناء عناصر الصفحة الآن فقط في الذاكرة
            view_control = self.routes[route_name]() 
            
            # إضافة الشاشة لنظام Views المتراكم والمناسب للهواتف
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

    def _handle_view_pop(self, e: ft.ViewPopEvent):
        """معالج زر الرجوع الفعلي للهاتف (Back Button) لمنع إغلاق التطبيق"""
        if len(self.page.views) > 1:
            self.page.views.pop()
            top_view = self.page.views[-1]
            self.page.go(top_view.route)
        else:
            # إذا كان في الصفحة الرئيسية وضغط رجوع، يرجع للمسار الأساسي أو يغلق
            self.page.go("/")
