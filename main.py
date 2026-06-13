import flet as ft
import time
import sys

# متغيرات عامة للخدمات
CURRENT_SERVICE = None
CURRENT_STEP = 0
PIN = ""
RECIPIENT = ""
AMOUNT = ""
PALPAY_ACCEPT_OPTION = "1"

def main(page: ft.Page):
    try:
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
            try:
                test_text.value = "تمت الاستجابة والنقر بنجاح! 🎉"
                test_button.text = "تم النقر ✓"
                page.update()
            except Exception as err:
                print(f"خطأ في زر النقر: {err}")
        
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
        
    except Exception as e:
        print(f"خطأ في تهيئة التطبيق: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        ft.app(target=main)
    except Exception as e:
        print(f"خطأ في تشغيل التطبيق: {e}")
        import traceback
        traceback.print_exc()
