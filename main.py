import flet as ft
from views.Home_view import Home_view  # استيراد واجهتك الذكية

def main(page: ft.Page):
    page.title = "USSD App"
    page.theme_mode = ft.ThemeMode.LIGHT

    # دالة معالجة المسارات بناءً على التوثيق الرسمي (Cookbook)
    def route_change(route):
        # استخدام TemplateRoute للمطابقة الذكية للمسارات
        troute = ft.TemplateRoute(page.route)
        
        page.views.clear()
        
        # إذا كان المسار هو الرئيسي، نقوم بدفع واجهتك فوراً
        if troute.match("/"):
            page.views.append(Home_view(page))
            
        page.update()

    # دالة التعامل مع زر الرجوع (Pop) لضمان عدم تجمد الأندرويد
    def view_pop(view):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            page.window_close()

    # ربط الأحداث بالصفحة كما توصي المقالة
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # التوجيه الافتراضي عند الإقلاع
    page.go(page.route)

ft.app(target=main)
