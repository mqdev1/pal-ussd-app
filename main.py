import flet as ft
import time
import sys

def main(page: ft.Page):
    # انتظام قصير لضمان استقرار اتصال فلاتر ببايثون في الخلفية
    time.sleep(1)
    
    # إعدادات الأندرويد الأساسية (بدون تحديد أبعاد النافذة window_width لأنها تسبب انهياراً على الجوال)
    page.title = "تطبيق USSD"
    page.rtl = True  # تفعيل الاتجاه العربي
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    
    # محتوى مرن وبسيط جداً للتأكد من اشتغال الواجهة
    page.add(
        ft.SafeArea( # تحمي العناصر من الاختفاء تحت شريط الإشعارات أو الكاميرا الأمامية
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=60),
                    ft.Text("تطبيق USSD يعمل بنجاح! 🚀", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    ft.Text("تم حل مشكلة الشاشة السوداء بنجاح.", size=14, color=ft.Colors.GREY_600),
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                expand=True
            )
        )
    )
    page.update()

if __name__ == "__main__":
    # تشغيل التطبيق بالوضع الافتراضي للأندرويد
    ft.app(target=main)
