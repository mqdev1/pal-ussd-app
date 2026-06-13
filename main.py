import flet as ft
import time

def main(page: ft.Page):
    # نمنح المحرك ثانية واحدة للاستقرار داخل نظام أندرويد
    time.sleep(1)
    
    # إعدادات أساسية متوافقة 100% مع الجوال
    page.title = "فحص الاتصال"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    
    try:
        # واجهة بسيطة جداً بدون أي تعقيد
        page.add(
            ft.SafeArea(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=60),
                            ft.Text("مرحباً محمود! التطبيق يعمل 🎉", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                            ft.Text("إذا رأيت هذه الشاشة، فالبيئة سليمة 100%", size=14, color=ft.Colors.GREY_600),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
            )
        )
    except s:
        page.add(
            ft.SafeArea(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("هناك خطاء يرجى مراجعته", size=14, color=ft.Colors.GREY_600),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
            )
        )
    page.update()
    
ft.app(target=main)
