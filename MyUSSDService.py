from jnius import autoclass

# استدعاء مكتبات أندرويد الأساسية للنظام عبر Pyjnius
AccessibilityEvent = autoclass('android.view.accessibility.AccessibilityEvent')
Bundle = autoclass('android.os.Bundle')

def onAccessibilityEvent(event):
    """
    هذه الدالة تراقب شاشات الـ USSD التابعة للنظام، وتقرأ الخطوة الحالية
    من ملف التطبيق الأساسي (main.py)، ثم تقوم بإدخال البيانات والضغط على إرسال تلقائياً.
    """
    import main  # استيراد المتغيرات الحية من تطبيق Flet الخاص بك
    
    # التفاعل فقط عندما تتغير الشاشة أو تظهر نافذة بوب-أب (Pop-up) جديدة للـ USSD
    if event.getEventType() == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED:
        source_node = event.getSource()
        if not source_node:
            return
            
        # تحديد حقل الإدخال وزر الإرسال الافتراضي في نظام أندرويد
        input_fields = source_node.findAccessibilityNodeInfosByViewId("com.android.phone:id/input_field")
        send_buttons = source_node.findAccessibilityNodeInfosByViewId("android:id/button1")
        
        # التأكد من وجود حقل الإدخال وزر الإرسال على الشاشة قبل بدئ العملية
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
            # الخدمة 1: نظام أتمتة بال بي (PalPay) - (محدث ليعمل على خطوتين)
            # =================================================================
            if main.CURRENT_SERVICE == "PALPAY":
                if main.CURRENT_STEP == 1:
                    # الخطوة 1: إدخال الرقم السري (PIN) في الشاشة الأولى
                    send_payload(main.PIN)
                    main.CURRENT_STEP = 2  # الانتقال للخطوة التالية (شاشة التأكيد)
                    
                elif main.CURRENT_STEP == 2:
                    # الخطوة 2: إدخال خيار التأكيد أو القبول (1 أو 2) حسب اختيار المستخدم
                    send_payload(main.PALPAY_ACCEPT_OPTION)
                    main.CURRENT_SERVICE = None  # إنهاء الجلسة وتصفير العدادات
                    main.CURRENT_STEP = 0

            # =================================================================
            # الخدمة 2: نظام أتمتة بنك فلسطين (BOP)
            # =================================================================
            elif main.CURRENT_SERVICE == "BOP":
                if main.CURRENT_STEP == 1:
                    send_payload("1")  # الخيار رقم 1 يمثل عادةً "تحويل أموال"
                    main.CURRENT_STEP = 2
                elif main.CURRENT_STEP == 2:
                    send_payload(main.RECIPIENT)  # إدخال رقم حساب المستلم
                    main.CURRENT_STEP = 3
                elif main.CURRENT_STEP == 3:
                    send_payload(main.AMOUNT)     # إدخال المبلغ المراد تحويله
                    main.CURRENT_STEP = 4
                elif main.CURRENT_STEP == 4:
                    send_payload(main.PIN)        # إدخال الرقم السري لإتمام العملية
                    main.CURRENT_SERVICE = None   # إنهاء الجلسة وتصفير العدادات
                    main.CURRENT_STEP = 0

            # =================================================================
            # الخدمة 3: نظام أتمتة جوال بي (JawwalPay)
            # =================================================================
            elif main.CURRENT_SERVICE == "JAWWAL":
                if main.CURRENT_STEP == 1:
                    send_payload("1")  # الخيار رقم 1 يمثل بدء عملية التحويل للمحافظ
                    main.CURRENT_STEP = 2
                elif main.CURRENT_STEP == 2:
                    send_payload(main.AMOUNT)     # إدخال قيمة المبلغ
                    main.CURRENT_STEP = 3
                elif main.CURRENT_STEP == 3:
                    send_payload(main.RECIPIENT)  # إدخال رقم هاتف المستلم (صاحب المحفظة)
                    main.CURRENT_STEP = 4
                elif main.CURRENT_STEP == 4:
                    send_payload(main.PIN)        # إدخال الرقم السري للمحفظة
                    main.CURRENT_SERVICE = None   # إنهاء الجلسة وتصفير العدادات
                    main.CURRENT_STEP = 0
