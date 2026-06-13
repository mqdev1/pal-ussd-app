import flet as ft
import time
import sys
import traceback

# متغيرات عامة للخدمات
CURRENT_SERVICE = None
CURRENT_STEP = 0
PIN = ""
RECIPIENT = ""
AMOUNT = ""
PALPAY_ACCEPT_OPTION = "1"

def main(page: ft.Page):
    try:
        # إعدادات الشاشة الأساسية وتفعيل الدعم العربي الكامل
        page.title = "تطبيق USSD"
        page.rtl = True  # تفعيل اتجاه النص من اليمين إلى اليسار للغة العربية
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        page.spacing = 20
        page.bgcolor = ft.Colors.WHITE
        
        # تعيين الضبط الاتجاهي
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        print("✓ تم تهيئة الصفحة بنجاح")
        
        # دالة عند النقر على الزر
        def button_click(e):
            try:
                test_text.value = "تمت الاستجابة والنقر بنجاح! 🎉"
                test_button.text = "تم النقر ✓"
                test_button.disabled = True
                page.update()
                print("✓ تم النقر على الزر بنجاح")
            except Exception as err:
                print(f"✗ خطأ في زر النقر: {err}")
                traceback.print_exc()
        
        # إنشاء عناصر الواجهة
        header = ft.Text(
            value="تطبيق USSD", 
            size=28, 
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700,
            text_align=ft.TextAlign.CENTER
        )
        
        test_text = ft.Text(
            value="تطبيق فحص الحد الأدنى (عامل بنجاح) ✓", 
            size=18, 
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK,
            text_align=ft.TextAlign.CENTER
        )
        
        status_text = ft.Text(
            value="الحالة: جاهز للعمل",
            size=14,
            color=ft.Colors.GREEN_600,
            text_align=ft.TextAlign.CENTER
        )
        
        test_button = ft.ElevatedButton(
            text="اضغط هنا للفحص 🚀",
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            on_click=button_click,
            width=300,
            height=50
        )
        
        divider = ft.Divider(color=ft.Colors.GREY_300, height=20)
        
        info_text = ft.Text(
            value="هذا التطبيق يختبر واجهة Flet على Android",
            size=12,
            color=ft.Colors.GREY_700,
            text_align=ft.TextAlign.CENTER,
            italic=True
        )
        
        # استخدام Column بداخل Container لضمان استقرار الأبعاد على الجوال
        main_container = ft.Column(
            controls=[
                header,
                divider,
                test_text,
                status_text,
                test_button,
                divider,
                info_text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True # جعل العمود يتمدد لملء الشاشة لمنع الشاشة السوداء
        )
        
        # إضافة المحتوى إلى الصفحة
        page.add(main_container)
        page.update()
        print("✓ تم إضافة العناصر إلى الصفحة بنجاح")
        
    except Exception as e:
        print(f"✗ خطأ في تهيئة التطبيق: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        print("🚀 بدء تطبيق USSD على الأندرويد...")
        # التعديل الجوهري: تشغيل التطبيق كـ Assets View ليتناسب مع جافا وأندرويد
        ft.app(target=main, view=ft.AppView.FLET_APP)
    except Exception as e:
        print(f"✗ خطأ في تشغيل التطبيق: {e}")
        traceback.print_exc()
        sys.exit(1)
