import flet as ft

def main(page: ft.Page):
    # 1. إعدادات الصفحة الأساسية (تُنفذ فوراً بدون تأخير)
    page.title = "فحص الاتصال"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    
    # ضبط المحاذاة لتوسيط المحتوى تماماً
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # 2. تحديث أولي لإرسال الإشارات للمحرك ومنع التجمد
    page.update()
    
    try:
        # 3. بناء الواجهة بشكل آمن وصحيح للموبايل
        page.add(
            ft.SafeArea(
                expand=True, # الآن آمن لأن الصفحة تم تحديثها واستقرت أبعادها
                content=ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=60),
                            ft.Text("مرحباً محمود! التطبيق يعمل 🎉", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                            ft.Text("البيئة الآن مستقرة وسليمة 100%", size=14, color=ft.Colors.GREY_600),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        tight=True # يمنع العمود من التمدد اللانهائي داخل الـ Container
                    )
                )
            )
        )
        # تحديث نهائي لإظهار العناصر
        page.update()
        
    except Exception as e:
        # في حال حدوث أي خطأ في الرندرة، يعرضه فوراً
        page.controls.clear()
        page.add(
            ft.Text(f"حدث خطأ غير متوقع: {str(e)}", color=ft.Colors.RED_700, size=16)
        )
        page.update()

# تشغيل التطبيق (تأكد من وجود مجلد assets لو قمت بتفعيله لاحقاً)
ft.app(target=main)
