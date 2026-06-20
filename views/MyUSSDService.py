from jnius import autoclass

# استدعاء مكتبات أندرويد الأساسية
AccessibilityEvent = autoclass('android.view.accessibility.AccessibilityEvent')
Bundle = autoclass('android.os.Bundle')

def onAccessibilityEvent(event):
    """
    هذه الدالة تراقب شاشات الـ USSD التابعة للنظام، وتقرأ الخطوة الحالية
    من ملف العرض (home_view)، ثم تقوم بإدخال البيانات والضغط على إرسال تلقائياً.
    """
    import home_view  # استيراد المتغيرات الحية من موديول العرض لتحديث الحالات
    
    # التفاعل فقط عندما تتغير الشاشة أو تظهر نافذة بوب-أب (Pop-up) جديدة للـ USSD
    if event.getEventType() == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED:
        source_node = event.getSource()
        if not source_node:
            return
            
        # تحديد حقل الإدخال وزر الإرسال الافتراضي في نظام أندرويد لـ USSD
        input_fields = source_node.findAccessibilityNodeInfosByViewId("com.android.phone:id/input_field")
        send_buttons = source_node.findAccessibilityNodeInfosByViewId("android:id/button1")
        
        # التأكد من وجود حقل الإدخال وزر الإرسال على الشاشة قبل بدء العملية
        if input_fields.size() > 0 and send_buttons.size() > 0:
            input_box = input_fields.get(0)
            send_btn = send_buttons.get(0)
            
            def send_payload(text_to_inject):
                """دالة مساعدة لكتابة النص داخل الحقل ومحاكاة ضغطة زر إرسال"""
                args = Bundle()
                # الكود 0x00200000 يمثل الأمر (ACTION_SET_TEXT) لإدخال النص
                args.putCharSequence("ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE", str(text_to_inject))
                input_box.performAction(0x00200000, args) 
                
                # الكود 16 يمثل الأمر (ACTION_CLICK) لمحاكاة الضغط
                send_btn.performAction(16)

            # =================================================================
            # الخدمة 1: نظام أتمتة جوال بي (JawwalPay)
            # =================================================================
            if home_view.CURRENT_SERVICE == "JAWWAL":
                if home_view.CURRENT_STEP == 1:
                    send_payload("1")  # الخيار رقم 1: تحويل أموال للمحافظ
                    home_view.CURRENT_STEP = 2
                elif home_view.CURRENT_STEP == 2:
                    send_payload(home_view.AMOUNT)     # إدخال قيمة المبلغ
                    home_view.CURRENT_STEP = 3
                elif home_view.CURRENT_STEP == 3:
                    send_payload(home_view.RECIPIENT)  # إدخال رقم هاتف المستلم الكامل
                    home_view.CURRENT_STEP = 4
                elif home_view.CURRENT_STEP == 4:
                    send_payload(home_view.PIN)        # إدخال الرقم السري للمحفظة
                    home_view.CURRENT_SERVICE = None   # تصفير الجلسة
                    home_view.CURRENT_STEP = 0

            # =================================================================
            # الخدمة 2: نظام أتمتة بنك فلسطين (BOP)
            # =================================================================
            elif home_view.CURRENT_SERVICE == "BOP":
                if home_view.CURRENT_STEP == 1:
                    send_payload("1")  # الخيار رقم 1 يمثل عادةً "تحويل أموال"
                    home_view.CURRENT_STEP = 2
                elif home_view.CURRENT_STEP == 2:
                    send_payload(home_view.RECIPIENT)  # إدخال رقم حساب/هاتف المستلم
                    home_view.CURRENT_STEP = 3
                elif home_view.CURRENT_STEP == 3:
                    send_payload(home_view.AMOUNT)     # إدخال المبلغ المراد تحويله
                    home_view.CURRENT_STEP = 4
                elif home_view.CURRENT_STEP == 4:
                    send_payload(home_view.PIN)        # إدخال الرقم السري لإتمام العملية
                    home_view.CURRENT_SERVICE = None   
                    home_view.CURRENT_STEP = 0

            # =================================================================
            # الخدمة 3: نظام أتمتة بال بي (PalPay) - معالجة السلسلة المباشرة
            # =================================================================
            elif home_view.CURRENT_SERVICE == "PALPAY":
                # بما أنك أرسلت السلسلة المباشرة المدمجة كاملة مثل (*370*1*1*الرقم*المبلغ#)
                # فإن الشاشة التي ستظهر ستطلب غالباً الرقم السري فقط أو التأكيد مباشرة
                if home_view.CURRENT_STEP == 1:
                    send_payload(home_view.PIN)  # إدخال الرقم السري في الشاشة الأولى المتوقعة
                    home_view.CURRENT_STEP = 2
                elif home_view.CURRENT_STEP == 2:
                    send_payload(home_view.PALPAY_ACCEPT_OPTION) # خيار التأكيد (1)
                    home_view.CURRENT_SERVICE = None   
                    home_view.CURRENT_STEP = 0
