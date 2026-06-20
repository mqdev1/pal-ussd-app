import flet as ft
from Router import Router

# تعريف متغيرات الحالة العامة (Global) لتتمكن خدمة الـ Accessibility من قراءتها وتعديلها حياً
CURRENT_SERVICE = None
CURRENT_STEP = 0
RECIPIENT = ""
AMOUNT = ""
PIN = ""
PALPAY_ACCEPT_OPTION = "1"

def home_view(page: ft.Page, route: Router) -> ft.Control:
    
    # دالة لفحص إذن إمكانية الوصول وطلبه مباشرة إذا لم يكن مفعلاً
    def check_and_request_accessibility():
        try:
            from jnius import autoclass
            
            # استدعاء كلاسات أندرويد المطلوبة
            Settings = autoclass('android.provider.Settings')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            
            activity = PythonActivity.mActivity
            content_resolver = activity.getContentResolver()
            
            # الفحص هل خدمات الوصول مفعلة بشكل عام
            accessibility_enabled = Settings.Secure.getInt(
                content_resolver, 
                Settings.Secure.ACCESSIBILITY_ENABLED, 
                0
            )
            
            # إذا لم تكن مفعلة، نقوم بفتح الإعدادات للمستخدم مباشرة لتفعيلها
            if accessibility_enabled == 0:
                page.snack_bar = ft.SnackBar(
                    ft.Text("يرجى تفعيل خدمة الوصول للتطبيق لتمكين الأتمتة التلقائية"), 
                    open=True
                )
                page.update()
                
                # فتح شاشة إعدادات خدمات إمكانية الوصول بالنظام
                intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)
                activity.startActivity(intent)
                
        except Exception as ex:
            print(f"Error checking accessibility permission: {ex}")

    def dial_ussd(code: str):
        try:
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
            Alert("USSD PAL", ex)

    # دالة موحدة لمعالجة الضغط على زر الإرسال بناءً على الخدمة المختارة
    def handle_send_click(e):
        global CURRENT_SERVICE, CURRENT_STEP, RECIPIENT, AMOUNT, PIN
        
        full_phone = f"05{phoneInput.value.strip()}"
        
        PIN = pin_input.value.strip()
        RECIPIENT = full_phone
        AMOUNT = amountInput.value.strip()
        CURRENT_STEP = 1  

        if serviceDDP.value == "JAWWAL":
            CURRENT_SERVICE = "JAWWAL"
            dial_ussd("*110#")
        elif serviceDDP.value == "BOP":
            CURRENT_SERVICE = "BOP"
            dial_ussd("*267#")
        elif serviceDDP.value == "PALPAY":
            CURRENT_SERVICE = "PALPAY"
            direct_string = f"*370*1*1*{full_phone}*{amountInput.value.strip()}#"
            dial_ussd(direct_string)

    phoneMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False, text_align=ft.TextAlign.RIGHT)
    amountMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False, text_align=ft.TextAlign.RIGHT)
    pinMessage = ft.Text("", color=ft.Colors.RED, size=14, visible=False, text_align=ft.TextAlign.RIGHT)

    serviceDDP = ft.Dropdown(
        expand=True,
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
                expand=True,
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

    def Alert(title, text):
        al = ft.AlertDialog(
            modal=False,
            title=ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
            content=ft.Text(text),
            actions=[ft.TextButton(text="حسناً", on_click=lambda _: page.close(al))]
        )
        page.open(al)

    def validateInputs():
        if not phoneInput.value or len(phoneInput.value) != 8:
            phoneMessage.value = "يرجى ادخال خانات رقم الهاتف الـ 8 المتبقية"
            phoneMessage.visible = True
            BtnSendMoney.disabled = True
        elif not phoneInput.value.startswith(('9', '6')):
            phoneMessage.value = "يجب ان يبدأ رقم الهاتف بعد الـ 05 بالرقم 9 او 6"
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

    bannerContainer = ft.Container(
        bgcolor=ft.Colors.GREEN_500,
        rtl=True,
        padding=10,
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
        hint_text='9xxxxxxx',
        color=ft.Colors.BLACK, 
        border_color=ft.Colors.TRANSPARENT, 
        expand=1,
        on_change=lambda _: validateInputs()
    )

    amountInput = ft.TextField(
        keyboard_type=ft.KeyboardType.NUMBER,
        color=ft.Colors.BLACK,
        border_color=ft.Colors.TRANSPARENT, 
        expand=1,
        on_change=lambda _: validateInputs()
    )

    pin_input = ft.TextField(
        keyboard_type=ft.KeyboardType.NUMBER,
        password=True,
        can_reveal_password=True,
        color=ft.Colors.BLACK,
        border_color=ft.Colors.TRANSPARENT, 
        expand=1,
        on_change=lambda _: validateInputs()
    )

    controlsContainer = ft.Container(
        padding=10,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                service_dropdown,
                ft.Container(padding=10),
                
                ft.Text("رقم الجوال", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.W_500),
                ft.Column(
                    spacing=3,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10,
                            padding=10,
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
                ft.Container(padding=10),
                ft.Text("المبلغ", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.W_500),
                ft.Column(
                    spacing=3,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10,
                            padding=10,
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
                ft.Container(padding=10),
                ft.Text("الرقم السري", size=15, color=ft.Colors.BLACK, weight=ft.FontWeight.W_500),
                ft.Column(
                    spacing=3,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            border_radius=10,
                            padding=10,
                            content=ft.Row(spacing=0, rtl=False, controls=[pin_input])
                        ),
                        pinMessage
                    ]
                ),
                ft.Container(padding=10),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[BtnSendMoney]
                )
            ]
        )
    )
    
    # الحاوية الأساسية للـ View
    main_container = ft.Container(
        padding=20,
        content=ft.Column(
            controls=[bannerContainer, controlsContainer],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        )
    )

    page.run_task(lambda: check_and_request_accessibility())
    
    return main_container
