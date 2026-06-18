import flet as ft
# ⚠️ قم بوضع أي مكتبات (Imports) كانت مستخدمة داخل home_view هنا في الأعلى
# مثل مكتبات الـ USSD أو الاتصالات إن وجدت.

def main(page: ft.Page):
    page.title = "USSD PAL - Home"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20 # يمكنك تعديله حسب رغبتك
    page.spacing = 10

    try:
        # -----------------------------------------------------------
        # 1. انقل المتغيرات والدوال الداخلية (مستمعات الأحداث) من home_view هنا
        # -----------------------------------------------------------
        def on_click_action(e):
            # مثال لدالة زر كانت موجودة في home_view
            print("Action triggered")
            page.update()

        # -----------------------------------------------------------
        # 2. انقل عناصر الواجهة (Controls) التي كانت داخل home_view هنا
        # -----------------------------------------------------------
        # على سبيل المثال، إذا كانت شاشتك تحتوي على أزرار وحقول نصية:
        ussd_input = ft.TextField(label="Enter USSD Code", hint_text="*123#")
        
        home_content = ft.Column(
            controls=[
                ft.Text("USSD PAL", size=24, weight=ft.FontWeight.BOLD),
                ussd_input,
                ft.ElevatedButton("Run Code", on_click=on_click_action),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # -----------------------------------------------------------
        # 3. إضافة الواجهة مباشرة إلى الصفحة
        # -----------------------------------------------------------
        page.add(home_content)

    except Exception as e:
        # هذا الـ try سيضمن طباعة أي خطأ برمي يحدث أثناء بناء عناصر الواجهة
        page.add(ft.Text(f"Error in Home View: {str(e)}", color="red", size=16))
    
    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')
