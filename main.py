import flet as ft
import time

def main(page: ft.Page):
    # إعدادات الشاشة الأساسية
    page.title = "تطبيق فحص"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.spacing = 20
    page.bgcolor = ft.Colors.WHITE
    
    # تعيين الضبط الاتجاهي
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # دالة عند النقر على الزر
    def button_click(e):
        test_text.value = "تمت الاستجابة والنقر بنجاح! 🎉"
        test_button.text = "تم النقر ✓"
        page.update()
    
    # إنشاء عناصر الواجهة
    test_text = ft.Text(
        value="تطبيق فحص الحد الأدنى (عامل بنجاح)", 
        size=24, 
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLACK,
        text_align=ft.TextAlign.CENTER
    )
    
    test_button = ft.ElevatedButton(
        text="اضغط هنا للفحص 🚀",
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        on_click=button_click,
        width=200,
        height=50
    )
    
    # إنشاء حاوية (Container) لتجنب مشاكل التصيير
    main_container = ft.Column(
        controls=[
            test_text,
            test_button
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        expand=True
    )
    
    # إضافة المحتوى إلى الصفحة
    page.add(main_container)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
