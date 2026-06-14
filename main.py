import flet as ft
# تأكد أن كلاس Home_view يرث من ft.View أو يعود بكائن ft.View(route="/", ...)
from views.Home_view import Home_view 

def main(page: ft.Page):
    # إعدادات الشاشة الأساسية لمنع التجمد
    page.title = "USSD PAL"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    try:
        # دالة معالجة تغيير المسارات (Route Change Handler)
        def change_route(route_event):
            # 1. نقوم بمسح الواجهات القديمة للبدء من جديد عند العودة للأصل
            page.views.clear()
            
            # 2. إضافة الصفحة الرئيسية دائماً كقاعدة أساسية في أسفل الـ Stack
            page.views.append(Home_view(page))
            
            # 3. إذا كان المسار الحالي مختلفاً عن الرئيسية، نقوم بإضافة الواجهة المطلوبة فوقها
            # مثال مستقبلي للتنقل:
            # if page.route == "/settings":
            #     page.views.append(SettingsView(page))
            
            # تحديث الشاشة لتطبيق التغييرات وعرض الواجهة النشطة في أعلى الـ Stack
            page.update()

        # دالة التراجع والعودة للخلف (Pop View Handler)
        def view_pop(view_event):
            # نقوم بالتراجع فقط إذا كان هناك أكثر من واجهة معروضة
            if len(page.views) > 1:
                page.views.pop() # حذف الواجهة العلوية
                top_view = page.views[-1] # الحصول على الواجهة التي أسفلها
                page.go(top_view.route) # الانتقال الآمن لمسار الواجهة السابقة
            else:
                page.go('/') # العودة للرئيسية كخيار احتياطي
            
        # ربط الأحداث بالدوال الخاصة بها
        page.on_route_change = change_route
        page.on_view_pop = view_pop
        
        # تشغيل التطبيق بالذهاب للمسار الرئيسي لأول مرة
        page.go('/')
        
    except Exception as ex:
        # تنظيف أي عناصر قديمة على الشاشة قبل عرض شاشة الخطأ
        page.views.clear()
        page.clean()
        
        # بناء شاشة عرض الخطأ الأنيقة
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
                        # أيقونة تحذيرية حمراء بتصميم دائري لطيف
                        ft.Icon(
                            name=ft.icons.ERROR_OUTLINE_ROUNDED,
                            color=ft.colors.RED_400,
                            size=80,
                        ),
                        # عنوان الخطأ الرئيسي
                        ft.Text(
                            "عذراً، حدث خطأ غير متوقع!",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLUE_GREY_900,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        # نص توضيحي للمستخدم
                        ft.Text(
                            "نواجه مشكلة مؤقتة في تشغيل النظام. يرجى مراجعة المطور أو المحاولة مرة أخرى.",
                            size=14,
                            color=ft.colors.BLUE_GREY_500,
                            text_align=ft.TextAlign.CENTER,
                            max_width=320,
                        ),
                        # صندوق يعرض تفاصيل الـ Exception التقنية بشكل منسق
                        ft.Container(
                            content=ft.Text(
                                f"رمز الخطأ:\n{str(ex)}",
                                size=12,
                                color=ft.colors.RED_800,
                                font_family="monospace",
                                text_align=ft.TextAlign.LEFT,
                            ),
                            bgcolor=ft.colors.RED_50,
                            padding=15,
                            border_radius=10,
                            border=ft.border.all(1, ft.colors.RED_100),
                            max_width=450,
                            width=page.width if page.width else 400,
                        ),
                        ft.Container(height=10), # مساحة تباعد بسيطة
                        # زر تفاعلي لإعادة تشغيل أو إنعاش التطبيق
                        ft.ElevatedButton(
                            text="إعادة المحاولة",
                            icon=ft.icons.REFRESH_ROUNDED,
                            bgcolor=ft.colors.BLUE_600,
                            color=ft.colors.WHITE,
                            on_click=lambda _: page.go("/"),
                            style=ft.ButtonStyle(
                                padding=ft.padding.all(18),
                                shape=ft.RoundedRectangleBorder(radius=10),
                            )
                        )
                    ]
                )
            )
        )
        page.update()
