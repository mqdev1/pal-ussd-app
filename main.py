import flet as ft
from views.Home_view import Home_view 

def main(page: ft.Page):
    # إعدادات الشاشة الأساسية لمنع التجمد
    page.title = "USSD PAL"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
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

# تشغيل التطبيق
if __name__ == "__main__":
    ft.app(target=main)
