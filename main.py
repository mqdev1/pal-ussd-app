import flet as ft
from views.test_view import test_view

def main(page: ft.Page):
    page.title = "Flet Routing App"

    # 1. تعريف قاموس الصفحات (Views Dictionary)
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

    # 2. معالجة تغيير الروت بناءً على التكديس التراكمي (Stack Routing)
    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        
        # دائماً نضع الـ Home كقاعدة للتطبيق في الأسفل
        page.views.append(views["/"]()) 
        
        # التأكد من سلامة الروت الحالي
        current_route = page.route if page.route else "/"
        
        if current_route != "/":
            if current_route in views:
                try:
                    # محاولة تحميل الصفحة المطلوبة بشكل آمن
                    page.views.append(views[current_route]())
                except Exception as ex:
                    print(f"Error loading view '{current_route}': {ex}")
                    # في حال حدوث خطأ، نغير الروت لـ /error لمنع تضارب التنقل ولضمان عمل زر الرجوع
                    page.route = "/error" 
                    page.views.append(
                        ft.View(
                            route="/error", 
                            controls=[
                                ft.AppBar(title=ft.Text("حدث خطأ ما"), bgcolor=ft.Colors.ERROR_CONTAINER),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.ERROR, size=50),
                                        ft.Text("تفاصيل المشكلة:", weight=ft.FontWeight.BOLD),
                                        ft.Text(f"{ex}", color=ft.Colors.ERROR),
                                        ft.ElevatedButton("العودة للرئيسية", on_click=lambda _: page.go("/"))
                                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    padding=20
                                )
                            ]
                        )
                    )
            else:
                # صفحة 404 في حال الروت غير موجود بالقاموس
                page.views.append(
                    ft.View(
                        route="/404", 
                        controls=[
                            ft.AppBar(title=ft.Text("الصفحة غير موجودة")),
                            ft.Text("404 - Page not found!"),
                            ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/"))
                        ]
                    )
                )
            
        page.update()

    # 3. معالجة زر الرجوع (Back Button)
    def view_pop(e: ft.ViewPopEvent):
        if len(page.views) > 1:
            page.views.pop() 
            top_view = page.views[-1] 
            page.route = top_view.route 
            page.update()

    # 4. تعيين الأحداث (Event Handlers)
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # 5. إطلاق التطبيق الآمن مع واجهة طوارئ عند فشل الإقلاع (Initialization Guard)
    try:
        initial_route = page.route if page.route in views else "/"
        page.go(initial_route)
    except Exception as initial_ex:
        # طباعة الخطأ للمطور في الـ Console
        print(f"Critical initialization error: {initial_ex}")
        
        # تنظيف شجرة الواجهات تماماً لبناء واجهة الخطأ الآمنة
        page.views.clear()
        page.route = "/critical-error"
        
        # عرض واجهة خطأ رسومية كاملة للمستخدم تمنع انهيار البرنامج
        page.views.append(
            ft.View(
                route="/critical-error",
                controls=[
                    ft.AppBar(
                        title=ft.Text("خطأ في تشغيل التطبيق", color=ft.Colors.WHITE), 
                        bgcolor=ft.Colors.RED_ACCENT_700,
                        automatically_imply_leading=False # إخفاء زر الرجوع الافتراضي
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.REPORT_PROBLEM_ROUNDED, color=ft.Colors.RED_ACCENT_400, size=80),
                            ft.Text("عذراً، تعذر تشغيل هذه الصفحة حالياً", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(f"تفاصيل الخطأ: {initial_ex}", color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER),
                            ft.VerticalDivider(height=20, color=ft.Colors.TRANSPARENT),
                            ft.ElevatedButton(
                                text="الانتقال للصفحة الرئيسية الآمنة",
                                icon=ft.Icons.HOME,
                                on_click=lambda _: page.go("/")
                            )
                        ], 
                        alignment=ft.MainAxisAlignment.CENTER, 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=30,
                        expand=True
                    )
                ]
            )
        )
        page.update()

ft.app(target=main)
