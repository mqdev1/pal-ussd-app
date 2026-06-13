import flet as ft
import time

def main(page: ft.Page):
    # وقت مستقطع قصير لضمان استقرار المحرك في الخلفية
    time.sleep(1) 
    
    page.title = "USSD App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True # للغة العربية
    
    # عناصر بسيطة جداً للتأكد من العرض
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("تطبيق USSD جاهز", size=30, weight="bold"),
                ft.Icon(ft.Icons.CHECK_CIRCLE, color="green", size=50),
            ], alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            expand=True
        )
    )
    page.update()

if __name__ == "__main__":
    # لا تضع أي باراميترات إضافية هنا، اتركها افتراضية للأندرويد
    ft.app(target=main)
