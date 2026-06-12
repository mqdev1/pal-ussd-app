import flet as ft

def Home_view(page: ft.Page):

    # --- المتغيرات العالمية للتحكم في خطوات الـ USSD ---
    CURRENT_SERVICE = None       # نوع الخدمة: "BOP" أو "PALPAY" أو "JAWWAL"
    CURRENT_STEP = 0             # الخطوة الحالية في الـ State Machine
    RECIPIENT = ""               # رقم حساب أو هاتف المستلم
    AMOUNT = ""                  # المبلغ
    PIN = ""                     # الرقم السري
    PALPAY_ACCEPT_OPTION = "1"   # خيار التأكيد لـ PalPay (1 أو 2)

    def dial_ussd(code: str):
        # تأجيل استدعاء المكتبة إلى داخل الدالة لمنع تجمد التطبيق عند الإقلاع (ANR)
        try:
            from jnius import autoclass 
            
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            activity = PythonActivity.mActivity
            encoded_code = Uri.encode(code)
            intent = Intent(Intent.ACTION_CALL)
            intent.setData(Uri.parse(f"tel:{encoded_code}"))
            activity.startActivity(intent)
        except Exception as ex:
            print(f"Native Android Call Error: {ex}")
            Alert("خطأ في النظام", "لا يمكن تشغيل ميزة الاتصال خارج بيئة أندرويد.")

    def trigger_palpay(e):
        nonlocal CURRENT_SERVICE, CURRENT_STEP, PIN, PALPAY_ACCEPT_OPTION
        CURRENT_SERVICE = "PALPAY"
        CURRENT_STEP = 1
        PIN = pin_input.value
        PALPAY_ACCEPT_OPTION = "1" # تم التثبيت بشكل افتراضي آمن لحين استخدام الـ Control الخاص بك
        
        direct_string = f"*370*1*1*{phoneInput.value}*{amountInput.value}#"
        dial_ussd(direct_string)

    def trigger_bop(e):
        nonlocal CURRENT_SERVICE, CURRENT_STEP, RECIPIENT, AMOUNT, PIN
        CURRENT_SERVICE = "BOP"
        CURRENT_STEP = 1
        RECIPIENT, AMOUNT, PIN = phoneInput.value, amountInput.value, pin_input.value
        dial_ussd("*267#")

    def trigger_jawwal(e):
        nonlocal CURRENT_SERVICE, CURRENT_STEP, RECIPIENT, AMOUNT, PIN
        CURRENT_SERVICE = "JAWWAL"
        CURRENT_STEP = 1
        RECIPIENT, AMOUNT, PIN = phoneInput.value, amountInput.value, pin_input.value
        dial_ussd("*110#")

    phoneMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False, text_align=ft.TextAlign.RIGHT)
    amountMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False, text_align=ft.TextAlign.RIGHT)
    pinMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False, text_align=ft.TextAlign.RIGHT)

    BtnSendMoney = ft.ElevatedButton(
        content=ft.Container(
            padding=16,
            content=ft.Text("ارسال", size=17)
        ),
        disabled=True,
        bgcolor=ft.Colors.GREEN_600,
        color=ft.Colors.WHITE,
        on_click=trigger_jawwal
    )

    def Alert(title, text):
        al = ft.AlertDialog(
            modal=False,
            title=ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
            content=ft.Text(text),
            actions=[
                ft.TextButton(
                    text="حسناً",
                    on_click=lambda _: page.close(al)
                )
            ]
        )
        page.open(al)

    def validateInputs():
        if phoneInput.value == '' or len(phoneInput.value) != 8:
            phoneMessage.value = "يرجى ادخال رقم الهاتف المكون من 8 أرقام"
            phoneMessage.visible = True
            BtnSendMoney.disabled = True

        elif str(phoneInput.value)[0:1] != '9' and str(phoneInput.value)[0:1] != '6':
            phoneMessage.value = "يجب ان يبداء رقم الهاتف بالرقم 9 او 6"
            phoneMessage.visible = True
            BtnSendMoney.disabled = True
        
        elif amountInput.value == '' or amountInput.value == '0':
            amountMessage.value = "يرجى ادخال المبلغ"
            amountMessage.visible = True
            BtnSendMoney.disabled = True

        elif pin_input.value == '':
            pinMessage.value = 'ادخل الرقم السري'
            pinMessage.visible = True
            BtnSendMoney.disabled = True

        else:
            phoneMessage.value = ''
            phoneMessage.visible = False
            amountMessage.value = ''
            amountMessage.visible = False
            pinMessage.value = ''
            pinMessage.visible = False
            BtnSendMoney.disabled = False
        
        page.update()

    bannerContainer = ft.Container(
        bgcolor=ft.Colors.GREEN_500,
        rtl=True,
        padding=ft.padding.only(40, 30, 40, 30),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("جوال باي", size=30, color=ft.Colors.WHITE),
                ft.Text("اهلا بك في خدمة USSD التابعة لجوال باي يمكنك تحديد رقم الجوال والمبلغ", size=15, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER)
            ]
        )
    )

    phoneInput = ft.TextField(
        keyboard_type=ft.KeyboardType.PHONE, 
        hover_color=ft.Colors.TRANSPARENT, 
        bgcolor=ft.Colors.TRANSPARENT, 
        max_length=8, 
        color=ft.Colors.BLACK, 
        text_align=ft.TextAlign.LEFT, 
        border_color=ft.Colors.TRANSPARENT, 
        text_style=ft.TextStyle(size=20), 
        autofocus=True,
        expand=1,
        on_change=lambda _: validateInputs()
    )

    amountInput = ft.TextField(
        hover_color=ft.Colors.TRANSPARENT, 
        bgcolor=ft.Colors.TRANSPARENT,
        color=ft.Colors.BLACK,
        max_length=10,
        text_align=ft.TextAlign.LEFT, 
        border_color=ft.Colors.TRANSPARENT, 
        text_style=ft.TextStyle(size=20), 
        expand=1,
        on_change=lambda _: validateInputs()
    )

    pin_input = ft.TextField(
        hover_color=ft.Colors.TRANSPARENT, 
        bgcolor=ft.Colors.TRANSPARENT,
        color=ft.Colors.BLACK,
        max_length=10,
        text_align=ft.TextAlign.LEFT, 
        border_color=ft.Colors.TRANSPARENT, 
        text_style=ft.TextStyle(size=20), 
        expand=1,
        on_change=lambda _: validateInputs()
    )

    controlsContainer = ft.Container(
        padding=ft.padding.only(50, 20, 50, 20),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("رقم الجوال", size=15, color=ft.Colors.BLACK),
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
                                    ft.Text("05", size=20, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
                                    phoneInput
                                ]
                            )
                        ),
                        phoneMessage
                    ]
                ),
                ft.Container(padding=ft.padding.only(0, 10, 0, 10)),
                ft.Text("المبلغ", size=15, color=ft.Colors.BLACK),
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
                                    ft.Text("شيكل", size=16)
                                ]
                            )
                        ),
                        amountMessage
                    ]
                ),
                ft.Container(padding=ft.padding.only(0, 10, 0, 10)),
                ft.Text("الرقم السري", size=15, color=ft.Colors.BLACK),
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
                                rtl=False,
                                controls=[
                                    pin_input
                                ]
                            )
                        ),
                        pinMessage
                    ]
                ),
                ft.Container(padding=ft.padding.only(0, 10, 0, 10)),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        BtnSendMoney
                    ]
                )
            ]
        )
    )

    return ft.View(
        "/",
        padding=0,
        bgcolor='#f0f0f0',
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            bannerContainer,
            controlsContainer
        ]
    )
