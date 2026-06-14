import flet as ft
from jnius import autoclass

def Home_view(page: ft.Page) -> ft.View:
    # --- قاموس لإدارة حالة خطوات الـ USSD دون الحاجة لكلاس ---
    state = {
        "CURRENT_SERVICE": None,       # نوع الخدمة: "BOP" أو "PALPAY" أو "JAWWAL"
        "CURRENT_STEP": 0,             # الخطوة الحالية في الـ State Machine
        "RECIPIENT": "",               # رقم حساب أو هاتف المستلم
        "AMOUNT": "",                  # المبلغ
        "PIN": "",                     # الرقم السري
        "PALPAY_ACCEPT_OPTION": "1"    # خيار التأكيد لـ PalPay (1 أو 2)
    }

    def dial_ussd(code: str):
        # تأجيل الاستيراد لمنع انهيار التطبيق عند تشغيله على الكمبيوتر أثناء التطوير
        try:
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
            # تنبيه مخصص بديل لـ Alert لمنع مشاكل تعليق الواجهات
            Alert("تنبيه المحاكي", "أنت تعمل الآن خارج بيئة أندرويد. تم توليد كود الـ USSD بنجاح:\n" + code)

    def trigger_palpay(e):
        state["CURRENT_SERVICE"] = "PALPAY"
        state["CURRENT_STEP"] = 1
        state["PIN"] = pin_input.value
        state["PALPAY_ACCEPT_OPTION"] = "1"
        
        direct_string = f"*370*1*1*{phoneInput.value}*{amountInput.value}#"
        dial_ussd(direct_string)

    def trigger_bop(e):
        state["CURRENT_SERVICE"] = "BOP"
        state["CURRENT_STEP"] = 1
        state["RECIPIENT"] = phoneInput.value
        state["AMOUNT"] = amountInput.value
        state["PIN"] = pin_input.value
        dial_ussd("*267#")

    def trigger_jawwal(e):
        state["CURRENT_SERVICE"] = "JAWWAL"
        state["CURRENT_STEP"] = 1
        state["RECIPIENT"] = phoneInput.value
        state["AMOUNT"] = amountInput.value
        state["PIN"] = pin_input.value
        dial_ussd("*110#")

    # رسائل الخطأ تحت الحقول
    phoneMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False, text_align=ft.TextAlign.RIGHT)
    amountMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False, text_align=ft.TextAlign.RIGHT)
    pinMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False, text_align=ft.TextAlign.RIGHT)

    # زر الإرسال
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
        # التحقق من رقم الهاتف
        if not phoneInput.value or len(phoneInput.value) != 8:
            phoneMessage.value = "يرجى ادخال رقم الهاتف المكون من 8 أرقام"
            phoneMessage.visible = True
            BtnSendMoney.disabled = True

        elif not phoneInput.value.startswith(('9', '6')):
            phoneMessage.value = "يجب ان يبدأ رقم الهاتف بالرقم 9 او 6"
            phoneMessage.visible = True
            BtnSendMoney.disabled = True
        
        # التحقق من المبلغ
        elif not amountInput.value or amountInput.value == '0':
            phoneMessage.visible = False
            amountMessage.value = "يرجى ادخال المبلغ"
            amountMessage.visible = True
            BtnSendMoney.disabled = True

        # التحقق من الرقم السري
        elif not pin_input.value:
            phoneMessage.visible = False
            amountMessage.visible = False
            pinMessage.value = 'ادخل الرقم السري'
            pinMessage.visible = True
            BtnSendMoney.disabled = True

        else:
            # تصفير كل رسائل الخطأ وتفعيل الزر
            phoneMessage.visible = False
            amountMessage.visible = False
            pinMessage.visible = False
            BtnSendMoney.disabled = False
        
        page.update()

    # الحاوية العلوية (البانر)
    bannerContainer = ft.Container(
        bgcolor=ft.Colors.GREEN_500,
        rtl=True,
        padding=ft.padding.only(40, 30, 40, 30),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("جوال باي", size=30, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                ft.Text("اهلا بك في خدمة USSD التابعة لجوال باي يمكنك تحديد رقم الجوال والمبلغ", size=15, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER)
            ]
        )
    )

    # الحقول المدخلة مع تحديد لوحة المفاتيح الرقمية للأرقام والمبالغ
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
        keyboard_type=ft.KeyboardType.NUMBER,
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
        keyboard_type=ft.KeyboardType.NUMBER,
        password=True,
        can_reveal_password=True,
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

    # حاوية عناصر التحكم
    controlsContainer = ft.Container(
        padding=ft.padding.only(50, 20, 50, 20),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
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
                                    ft.Text("05", size=20, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
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
                ft.Container(padding=ft.padding.only(0, 15, 0, 15)),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        BtnSendMoney
                    ]
                )
            ]
        )
    )
    
    # إرجاع كائن الـ View بشكل مباشر بدلاً من استخدام الوراثة في الكلاس
    return ft.View(
        route="/",
        padding=0,
        bgcolor='#f0f0f0',
        controls=[
            bannerContainer,
            controlsContainer
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH
    )
