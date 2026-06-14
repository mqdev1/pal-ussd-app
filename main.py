import flet as ft
import time

def main(page: ft.Page):
    # نمنح المحرك ثانية واحدة للاستقرار داخل نظام أندرويد
    time.sleep(1)
    
    # إعدادات أساسية متوافقة 100% مع الجوال
    page.title = "فحص الاتصال"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # ضبط محاذاة الصفحة الأساسية لضمان التوسط التام
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    try:
        # واجهة بسيطة جداً بدون أي تعقيد مع تأمين أبعاد المحرك
        page.controls.clear()
        page.add(
            ft.SafeArea(
                expand=True,
                content=ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=60),
                            ft.Text("مرحباً محمود! التطبيق يعمل 🎉", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                            ft.Text("إذا رأيت هذه الشاشة، فالبيئة سليمة 100%", size=14, color=ft.Colors.GREY_600),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            )
        )
        page.update()
        
    except Exception as e: # التعديل الجوهري هنا
        # في حال حدوث أي خطأ غريب أثناء الرندرة، يفرغ الصفحة ويعرض الخطأ الحقيقي
        page.controls.clear()
        page.add(
            ft.SafeArea(
                expand=True,
                content=ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED, size=60),
                            ft.Text("هناك خطأ يرجى مراجعته", size=18, color=ft.Colors.RED, weight=ft.FontWeight.BOLD),
                            ft.Text(f"تفاصيل الخطأ: {str(e)}", size=12, color=ft.Colors.GREY_700) # يطبع لك الخطأ على الشاشة بدقة
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            )
        )
        page.update()
    
ft.app(target=main, assets_dir='assets')
