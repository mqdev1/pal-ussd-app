import flet as ft

def main(page: ft.Page):
    page.title = "USSD PAL"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.bgcolor = ft.Colors.GREY_100 # لتجنب البياض المفاجئ

    state = {
        "CURRENT_SERVICE": "JAWWAL",
        "RECIPIENT": "",
        "AMOUNT": "",
        "PIN": ""
    }

    def Alert(title, text):
        al = ft.AlertDialog(
            title=ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
            content=ft.Text(str(text)),
            actions=[ft.TextButton(text="حسناً", on_click=lambda _: page.close(al))]
        )
        page.open(al)

    def dial_ussd(code: str):
        try:
            clean_code = code.replace("#", "%23")
            page.launch_url(f"tel:{clean_code}")
        except Exception as ex:
            Alert("خطأ", ex)

    def handle_send_click(e):
        state["PIN"] = pin_input.value
        state["RECIPIENT"] = phoneInput.value
        state["AMOUNT"] = amountInput.value

        if serviceDDP.value == "JAWWAL":
            dial_ussd("*110#")
        elif serviceDDP.value == "BOP":
            dial_ussd("*267#")
        elif serviceDDP.value == "PALPAY":
            direct_string = f"*370*1*1*{phoneInput.value}*{amountInput.value}#"
            dial_ussd(direct_string)

    phoneMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False)
    amountMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False)
    pinMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False)

    def validateInputs():
        if not phoneInput.value or len(phoneInput.value) != 8:
            phoneMessage.value = "يرجى ادخال رقم الهاتف المكون من 8 أرقام"
            phoneMessage.visible = True
            BtnSendMoney.disabled = True
        elif not phoneInput.value.startswith(('9', '6')):
            phoneMessage.value = "يجب ان يبدأ رقم الهاتف بالرقم 9 او 6"
            phoneMessage.visible = True
            BtnSendMoney.disabled = True
        elif not amountInput.value or amountInput.value == '0':
            phoneMessage.visible = False
            amountMessage.value = "يرجى ادخال المبلغ"
            amountMessage.visible = True
            BtnSendMoney.disabled = True
        elif not pin_input.value:
            phoneMessage.visible = False
            amountMessage.visible = False
            pinMessage.value = 'ادخل الرقم السري'
            pinMessage.visible = True
            BtnSendMoney.disabled = True
        else:
            phoneMessage.visible = False
            amountMessage.visible = False
            pinMessage.visible = False
            BtnSendMoney.disabled = False
        page.update()

    serviceDDP = ft.Dropdown(
        value="JAWWAL",
        color=ft.Colors.BLACK,
        border_color=ft.Colors.TRANSPARENT,
        options=[
            ft.dropdown.Option("JAWWAL", "جوال باي (Jawwal Pay)"),
            ft.dropdown.Option("BOP", "بنك فلسطين (BOP)"),
            ft.dropdown.Option("PALPAY", "بال بي (PalPay)"),
        ]
    )

    service_dropdown = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls = [
            ft.Text("اختر نوع الخدمة", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.W_500),
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                content=serviceDDP
            )
        ]
    )

    # تعديل الزر ليتمدد برمجياً بشكل آمن وبدون Container داخلي معقد
    BtnSendMoney = ft.ElevatedButton(
        text="ارسال",
        style=ft.ButtonStyle(
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        disabled=True,
        bgcolor=ft.Colors.GREEN_600,
        color=ft.Colors.WHITE,
        on_click=handle_send_click 
    )

    bannerContainer = ft.Container(
        bgcolor=ft.Colors.GREEN_500,
        rtl=True,
        padding=ft.padding.only(40, 30, 40, 30),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("بوابة USSD PAL", size=30, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                ft.Text("أهلاً بك، الرجاء تحديد نوع الخدمة وإدخال البيانات المطلوبة لإتمام العملية", size=14, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER)
            ]
        )
    )

    phoneInput = ft.TextField(
        keyboard_type=ft.KeyboardType.PHONE, 
        max_length=8, 
        color=ft.Colors.BLACK, 
        border_color=ft.Colors.TRANSPARENT, 
        on_change=lambda _: validateInputs()
    )

    amountInput = ft.TextField(
        keyboard_type=ft.KeyboardType.NUMBER,
        color=ft.Colors.BLACK,
        max_length=10,
        border_color=ft.Colors.TRANSPARENT, 
        on_change=lambda _: validateInputs()
    )

    pin_input = ft.TextField(
        keyboard_type=ft.KeyboardType.NUMBER,
        password=True,
        can_reveal_password=True,
        color=ft.Colors.BLACK,
        max_length=10,
        border_color=ft.Colors.TRANSPARENT, 
        on_change=lambda _: validateInputs()
    )

    controlsContainer = ft.Container(
        padding=ft.padding.only(50, 20, 50, 20),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15, # توزيع المسافات بشكل تلقائي آمن بدلاً من تكرار Containers فارغة
            controls=[
                service_dropdown,
                
                ft.Text("رقم الجوال", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.W_500),
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    padding=ft.padding.only(15, 0, 15, 0),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            ft.Text("05", size=20, color=ft.Colors.BLACK),
                            ft.Container(content=phoneInput, expand=True) # التمدد المحمي هنا
                        ]
                    )
                ),
                phoneMessage,
                
                ft.Text("المبلغ", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.W_500),
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    padding=ft.padding.only(15, 0, 15, 0),
                    content=ft.Row(
                        controls=[
                            ft.Container(content=amountInput, expand=True),
                            ft.Text("شيكل", size=16, color=ft.Colors.BLACK)
                        ]
                    )
                ),
                amountMessage,
                
                ft.Text("الرقم السري", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.W_500),
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    padding=ft.padding.only(15, 0, 15, 0),
                    content=pin_input # الـ TextField مباشرة هنا لا يحتاج Row طالما هو لوحده
                ),
                pinMessage,
                
                # جعل الزر يتمدد بعرض الشاشة بشكل آمن جداً للأندرويد
                ft.Row(
                    controls=[BtnSendMoney],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ]
        )
    )

    # بناء الصفحة داخل دالة حماية قصوى
    try:
        page.add(
            ft.Column(
                controls=[bannerContainer, controlsContainer],
                scroll=ft.ScrollMode.AUTO # إضافة سكرول تلقائي لمنع الـ Overflow على الشاشات الصغيرة
            )
        )
    except Exception as e:
        page.add(ft.Text(f"Layout Error: {e}", color="red"))
        
    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')
