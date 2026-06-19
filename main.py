import flet as ft
import asyncio
from views.home_view import home_view
from views.test_view import test_view
from Router import Router

# تحويل الدالة إلى async لمنع تجمد التطبيق أثناء شاشة الترحيب
async def main(page: ft.Page):

    route_log = ft.Column(controls=[ft.Text(f"Initial route: {page.route}")])
    page.add(ft.SafeArea(content=route_log))


    page.title = "USSD PAL"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0

    try:
        # إنشاء كائن الـ Router
        router = Router(page)

        # تسجيل الصفحات كمراجع (لاحظ استخدام lambda لمنع التنفيذ الفوري)
        router.register_route("welcome_view", lambda: ft.Container(
            expand=True, # يجعله يتمدد ليأخذ كامل الشاشة
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER, # لتوسيط النصوص عمودياً داخل الكولوم
                controls=[
                    ft.Text("Welcome to USSD PAL", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Will start in 3 Seconds...", size=12),
                ]
            )
        ))
        
        router.register_route("home_view", lambda: home_view(page, router))

        #router.register_route("test_view", lambda: test_view(page, router))

        # التوجه لشاشة الترحيب
        router.go_to("welcome_view")

        # الانتظار بشكل ذكي دون تجميد الواجهة (Main Thread)
        await asyncio.sleep(3) 

        # الانتقال للرئيسية
        router.go_to("home_view")
    except Exception as ex:
        page.add(ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(F"هناك خطاء [{ex}]")
                ]
            )
        ))

ft.run(main, assets_dir='assets')
