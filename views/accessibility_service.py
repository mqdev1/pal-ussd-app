import home_view  # لاستيراد المتغيرات العامة الحية (CURRENT_SERVICE, PIN, RECIPIENT...)

def on_accessibility_event(event):
    try:
        from jnius import autoclass, cast
        
        # كلاسات أندرويد لإدارة نوافذ وعناصر الشاشة
        AccessibilityEvent = autoclass('android.view.accessibility.AccessibilityEvent')
        AccessibilityNodeInfo = autoclass('android.view.accessibility.AccessibilityNodeInfo')
        Bundle = autoclass('android.os.Bundle')
        
        # نراقب فقط أحداث تغير النوافذ (ظهور صندوق الـ USSD)
        if event.getEventType() != AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED:
            return

        source = event.getSource()
        if source is None:
            return

        # البحث عن حقول إدخال النص والأزرار في النافذة المنبثقة
        input_fields = source.findAccessibilityNodeInfosByViewId("amigo:id/edit") # لبعض الهواتف المعدلة
        if not input_fields or input_fields.size() == 0:
            input_fields = source.findAccessibilityNodeInfosByText("") # البحث العام عن أي حقل إدخال
            
        send_buttons = source.findAccessibilityNodeInfosByText("إرسال")
        if not send_buttons or send_buttons.size() == 0:
            send_buttons = source.findAccessibilityNodeInfosByText("Send")

        if input_fields and input_fields.size() > 0 and send_buttons and send_buttons.size() > 0:
            input_node = input_fields.get(0)
            send_node = send_buttons.get(0)
            
            # --- أتمتة جوال باي (JAWWAL) ---
            if home_view.CURRENT_SERVICE == "JAWWAL":
                if home_view.CURRENT_STEP == 1:
                    # الخطوة 1: اختيار خيار "تحويل أموال" (مثلاً رقم 1)
                    fill_text_and_send(input_node, send_node, "1", Bundle)
                    home_view.CURRENT_STEP = 2
                elif home_view.CURRENT_STEP == 2:
                    # الخطوة 2: إدخال رقم المستلم الممرر من الواجهة
                    fill_text_and_send(input_node, send_node, home_view.RECIPIENT, Bundle)
                    home_view.CURRENT_STEP = 3
                elif home_view.CURRENT_STEP == 3:
                    # الخطوة 3: إدخال المبلغ
                    fill_text_and_send(input_node, send_node, home_view.AMOUNT, Bundle)
                    home_view.CURRENT_STEP = 4
                elif home_view.CURRENT_STEP == 4:
                    # الخطوة الأخيرة: إدخال الرقم السري لتأكيد العملية
                    fill_text_and_send(input_node, send_node, home_view.PIN, Bundle)
                    home_view.CURRENT_SERVICE = None  # إنهاء العملية
            
            # --- أتمتة بنك فلسطين (BOP) ---
            elif home_view.CURRENT_SERVICE == "BOP":
                if home_view.CURRENT_STEP == 1:
                    fill_text_and_send(input_node, send_node, "1", Bundle) # خيار التحويل
                    home_view.CURRENT_STEP = 2
                elif home_view.CURRENT_STEP == 2:
                    fill_text_and_send(input_node, send_node, home_view.RECIPIENT, Bundle)
                    home_view.CURRENT_STEP = 3
                elif home_view.CURRENT_STEP == 3:
                    fill_text_and_send(input_node, send_node, home_view.AMOUNT, Bundle)
                    home_view.CURRENT_STEP = 4
                elif home_view.CURRENT_STEP == 4:
                    fill_text_and_send(input_node, send_node, home_view.PIN, Bundle)
                    home_view.CURRENT_SERVICE = None
            
            # --- أتمتة بال بي (PALPAY) ---
            elif home_view.CURRENT_SERVICE == "PALPAY":
                if home_view.CURRENT_STEP == 1:
                    # بال بي تم بدء الاتصال بها ككود مركب مسبقاً، هنا يطلب فقط خيار التأكيد أو الرقم السري
                    fill_text_and_send(input_node, send_node, home_view.PALPAY_ACCEPT_OPTION, Bundle)
                    home_view.CURRENT_STEP = 2
                elif home_view.CURRENT_STEP == 2:
                    fill_text_and_send(input_node, send_node, home_view.PIN, Bundle)
                    home_view.CURRENT_SERVICE = None

    except Exception as e:
        print(f"Error in accessibility automation layer: {e}")

# دالة مساعدة لحقن النص داخل الحقل والضغط على زر الإرسال برمجياً
def fill_text_and_send(input_node, send_node, text, BundleClass):
    arguments = BundleClass()
    arguments.putCharSequence("ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE", text)
    # تنفيذ عملية كتابة النص
    input_node.performAction(16384, arguments) # 16384 تعني ACTION_SET_TEXT في أندرويد
    # تنفيذ عملية الضغط على الزر
    send_node.performAction(16) # 16 تعني ACTION_CLICK في أندرويد
