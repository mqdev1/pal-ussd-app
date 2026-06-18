import flet as ft

def main(page: ft.Page):
    page.title = "USSD PAL"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.bgcolor = ft.Colors.grey_100  # خلفية مريحة للعين لتفادي بياض الشاشة الكامل

    # الحفاظ على حالة التطبيق (State)
    state = {
        "CURRENT_SERVICE": "JAWWAL",
        "CURRENT_STEP": 0,
        "RECIPIENT": "",
        "AMOUNT": "",
        "PIN": "",
        "PALPAY_ACCEPT_OPTION": "1"
    }

    # دالة التنبيهات (AlertDialog)
    def Alert(title, text):
        al = ft.AlertDialog(
            modal=False,
            title=ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
            content=ft.Text(str(text)),
            actions=[ft.TextButton(text="حسناً", on_click=lambda _: page.close(al))]
        )
        page.open(al)

    # دالة تشغيل كود USSD (معدلة لتجنب الشاشة البيضاء)
    def dial_ussd(code: str):
        try:
            # تم نقل الـ import هنا لضمان عدم انهيار التطبيق أثناء الإقلاع
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            activity = PythonActivity.mActivity
            encoded_code = Uri.encode(code)
            intent = Intent(Intent.ACTION_DIAL)
            intent.setData(Uri.parse(f"tel:{encoded_code}"))
            activity.startActivity(intent)
        except Exception as ex:
            print(f"Native Android Call Error: {ex}")
            Alert("خطأ في النظام (Android Error)", f"فشل استدعاء اتصال النظام. السبب المحتمل: البيئة ليست أندرويد أو نقص مكتبة jnius.\nالتفاصيل: {ex}")

    # معالجة الضغط على زر الإرسال
    def handle_send_click(e):
        state["PIN"] = pin_input.value
        state["RECIPIENT"] = phoneInput.value
        state["AMOUNT"] = amountInput.value

        if serviceDDP.value == "JAWWAL":
            state["CURRENT_SERVICE"] = "JAWWAL"
            dial_ussd("*110#")
        elif serviceDDP.value == "BOP":
            state["CURRENT_SERVICE"] = "BOP"
            dial_ussd("*267#")
        elif serviceDDP.value == "PALPAY":
            state["CURRENT_SERVICE"] = "PALPAY"
            direct_string = f"*370*1*1*{phoneInput.value}*{amountInput.value}#"
            dial_ussd(direct_string)

    # رسائل الخطأ والتحقق
    phoneMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False, text_align=ft.TextAlign.RIGHT)
    amountMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False, text_align=ft.TextAlign.RIGHT)
    pinMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False, text_align=ft.TextAlign.RIGHT)

    # التحقق من المدخلات
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

    # عناصر واجهة المستخدم (UI Controls)
    serviceDDP = ft.Dropdown(
        label_style=ft.TextStyle(color=ft.Colors.BLACK),
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
        controls=[
            ft.Text("اختر نوع الخدمة", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.W_500),
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                content=serviceDDP
            )
        ]
    )

    BtnSendMoney = ft.ElevatedButton(
        content=ft.Container(
            padding=16,
            content=ft.Text("ارسال", size=17)
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
        expand=1,
        on_change=lambda _: validateInputs()
    )

    amountInput = ft.TextField(
        keyboard_type=ft.KeyboardType.NUMBER,
        color=ft.Colors.BLACK,
        max_length=10,
        border_color=ft.Colors.TRANSPARENT, 
        expand=1,
        on_change=lambda _: validateInputs()
    )

    pin_input = ft.TextField(
        keyboard_type=ft.KeyboardType.NUMBER,
        password=True,
        can_reveal_password=True,
        color=ft.Colors.BLACK,
        max_length=10,
        border_color=ft.Colors.TRANSPARENT, 
        expand=1,
        on_change=lambda _: validateInputs()
    )

    controlsContainer = ft.Container(
        padding=ft.padding.only(50, 20, 50, 20),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                service_dropdown,
                ft.Container(padding=ft.padding.only(0, 5, 0, 5)),
                ft.Text("رقم الجوال", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.W_500),
                ft.Column(
                    spacing=3,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10,
                            padding=ft.padding.only(10, 0, 10, 0),
                            content=ft.Row(
                                spacing=0,
                                rtl=False,
                                controls=[
                                    ft.Text("05", size=20, color=ft.Colors.BLACK),
                                    phoneInput
                                ]
                            )
                        ),
                        phoneMessage
                    ]
                ),
                ft.Container(padding=ft.padding.only(0, 10, 0, 10)),
                ft.Text("المبلغ", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.W_500),
                ft.Column(
                    spacing=3,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10,
                            padding=ft.padding.only(10, 0, 10, 0),
                            content=ft.Row(
                                spacing=0,
                                controls=[
                                    amountInput,
                                    ft.Text("شيكل", size=16, color=ft.Colors.BLACK)
                                ]
                            )
                        ),
                        amountMessage
                    ]
                ),
                ft.Container(padding=ft.padding.only(0, 10, 0, 10)),
                ft.Text("الرقم السري", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.W_500),
                ft.Column(
                    spacing=3,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10,
                            padding=ft.padding.only(10, 0, 10, 0),
                            content=ft.Row(spacing=0, rtl=False, controls=[pin_input])
                        ),
                        pinMessage
                    ]
                ),
                ft.Container(padding=ft.padding.only(0, 15, 0, 15)),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[BtnSendMoney]
                )
            ]
        )
    )

    # تجميع وحقن الواجهة في الصفحة مباشرة
    try:
        page.add(
            ft.Column(
                controls=[bannerContainer, controlsContainer],
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH
            )
        )
    except Exception as e:
        page.add(ft.Text(f"UI Error: {e}", color="red"))
        
    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')
