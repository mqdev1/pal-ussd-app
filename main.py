import flet as ft

def main(page: ft.Page):
    # إعدادات بسيطة للشاشة
    page.title = "Flet Minimum Test"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # تنظيف الواجهة تماماً
    page.controls.clear()

    # دالة بسيطة عند النقر على الزر لتغيير النص للـ فحص
    def button_click(e):
        test_text.value = "تمت الاستجابة والنقر بنجاح! 🎉"
        page.update()

    # عناصر الواجهة المباشرة
    test_text = ft.Text(
        value="تطبيق فحص الحد الأدنى (عامل بنجاح)", 
        size=20, 
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLACK
    )
    
    test_button = ft.ElevatedButton(
        text="اضغط هنا للفحص 🚀",
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        on_click=button_click
    )

    # إضافة العناصر مباشرة إلى قائمة التحكم الأساسية للـ page
    page.add(test_text, test_button)
    
    # إجبار محرك الرندرة على الرسم فوراً
    page.update()

ft.app(target=main)
