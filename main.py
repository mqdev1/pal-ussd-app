import flet as ft
from views.HomeView import HomeView 

def main(page: ft.Page):
    page.title = "USSD PAL"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    
    # 1. دالة معالجة تغيير المسارات بطريقة آمنة
    def change_route(route_event):
        # التحقق الآمن للمسار الرئيسي
        if page.route == "/":
            page.views.clear()
            page.views.append(HomeView(page))
        
        # يمكنك إضافة المسارات الأخرى هنا مستقبلاً
        # elif page.route == "/settings":
        #     page.views.append(SettingsView(page))
            
        page.update()

    # 2. دالة التراجع للخلف (عند الضغط على زر الرجوع في الهاتف)
    def view_pop(view_event):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            page.go('/')
        
    # 3. ربط الأحداث بالدوال الخاصة بها
    page.on_route_change = change_route
    page.on_view_pop = view_pop
    
    # 4. التفعيل الآمن لأول شاشة: 
    # نقوم باستدعاء الدالة مباشرة لبناء الشاشة الرئيسية فوراً دون استدعاء page.go المسببة للمشاكل
    change_route(None)

if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')
