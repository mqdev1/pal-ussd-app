import flet as ft
from views.test_view import test_view

def main(page: ft.Page):
    page.title = "Mobile Routing Example"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # 1. معالجة تغيير الروت (بناء الـ Stack)
    def route_change(e: ft.RouteChangeEvent):
        # في كل تغيير روت، نمسح القائمة لنعيد بناء الهيكل الصحيح من الأسفل للأعلى
        page.views.clear()
        
        # [دائماً وأبداً] الصفحة الرئيسية هي القاعدة في أسفل الـ Stack
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.AppBar(title=ft.Text("Home Screen"), bgcolor=ft.Colors.SURFACE_TINT),
                    ft.ElevatedButton("Go to Settings", on_click=lambda _: page.go("/settings")),
                    ft.ElevatedButton("Go to Test", on_click=lambda _: page.go("/test")),
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        
        # إذا طلب المستخدم الإعدادات، نضعها "فوق" الرئيسية
        if page.route == "/settings":
            page.views.append(
                ft.View(
                    route="/settings",
                    controls=[
                        ft.AppBar(title=ft.Text("Settings"), bgcolor=ft.Colors.SURFACE_TINT),
                        ft.Text("Welcome to the settings screen!"),
                        ft.ElevatedButton("Go Back", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        
        # إذا طلب صفحة التيست، نضعها أيضاً "فوق" الرئيسية
        elif page.route == '/test':
            # تأكد أن دالة test_view تعيد كائن من نوع ft.View
            page.views.append(test_view(page))
        
        page.update()

    # 2. معالجة زر الرجوع (حذف الصفحة العلوية فقط)
    def view_pop(e: ft.ViewPopEvent):
        if len(page.views) > 1: # للتأكد من وجود صفحات يمكن الرجوع إليها
            page.views.pop() # حذف الصفحة الحالية من الأعلى
            top_view = page.views[-1] # الحصول على الصفحة التي أصبحت في الأعلى (الرئيسية مثلاً)
            
            # ملاحظة هامة جداً:
            # نغير الروت كـ نص فقط ولا نستخدم page.go() لمنع تكرار دالة route_change ودخول التطبيق في Loop
            page.route = top_view.route 
            page.update()

    # تعيين المستمعين للأحداث
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # تشغيل التطبيق على الروت الحالي
    page.go(page.route)

ft.app(target=main)
