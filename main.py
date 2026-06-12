import flet as ft
from views.Home_view import Home_view  # استيراد واجهتك الأصلية

def main(page: ft.Page):
    # 1. إعدادات الشاشة الأساسية والتصميم النظيف
    page.title = "USSD Direct Test"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0  # تصفير الحواف لملء الشاشة بالكامل مثل الـ View
    
    # تنظيف الواجهة تماماً قبل البدء
    page.controls.clear()

    try:
        # 2. استدعاء صفحتك الأساسية
        home_screen = Home_view(page)
        
        # 3. فحص الكائن المسترجع وإضافته للـ page مباشرة بدون Route
        # إذا كانت دالتك ترجع كائن ft.View (والذي يحتوي على خاصية controls)
        if hasattr(home_screen, "controls") and home_screen.controls:
            page.controls.extend(home_screen.controls)
            
            # إذا كان هناك AppBar أو FloatingActionButton داخل الـ View، ننقلهم للـ page
            if hasattr(home_screen, "appbar") and home_screen.appbar:
                page.appbar = home_screen.appbar
            if hasattr(home_screen, "floating_action_button") and home_screen.floating_action_button:
                page.floating_action_button = home_screen.floating_action_button
        else:
            # إذا كانت الدالة ترجع عناصر تحكم مباشرة أو كائن مخصص
            page.controls.append(home_screen)
            
        # تحديث الشاشة لإجبار محرك رندرة Flutter على الرسم فوراً
        page.update()

    except Exception as e:
        # حماية شاملة: إذا كان هناك أي سطر أو مكتبة تسبب كراش داخل Home_view ستظهر هنا باللون البرتقالي
        page.controls.clear()
        page.add(
            ft.Container(
                padding=20,
                margin=20,
                bgcolor=ft.Colors.ORANGE_900,
                border_radius=10,
                alignment=ft.alignment.center,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(name=ft.Icons.BUG_REPORT, size=40, color=ft.Colors.WHITE),
                        ft.Text("⚠️ تم رصد مشكلة داخل كود الواجهة:", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(str(e), color=ft.Colors.WHITE, size=13, selectable=True)
                    ]
                )
            )
        )
        page.update()

ft.app(target=main)
