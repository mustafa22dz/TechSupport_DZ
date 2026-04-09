import streamlit as st
import google.generativeai as genai

# 1. إعدادات واجهة الموقع
st.set_page_config(page_title="TechSupport_DZ", page_icon="💻")
st.title("TechSupport_DZ 🛠️")
st.write("مرحباً بك في منصة الدعم الفني الذكي.")

# 2. ربط الذكاء الاصطناعي بمفتاحك
# ملاحظة: Gemini 1.5 Flash هو النسخة المستقرة والمجانية الحالية
genai.configure(api_key="AIzaSyCjh9vUSX0nQ2jvKU4sZ6UtqVlL6-HILtc")
model = genai.GenerativeModel('gemini-pro')

# 3. التعليمات البرمجية (System Instruction)
system_instruction = "أنت خبير صيانة ويندوز ولابتوب، اسمك TechSupport_DZ. تجيب بوضوح وباللغة العربية مع خطوات مرتبة."

# 4. إعداد سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. استلام سؤال المستخدم ومعالجته
if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # الطريقة الصحيحة لإرسال التعليمات مع السؤال
        response = model.generate_content([system_instruction, prompt])
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    except Exception as e:
        # إذا حدث خطأ سيظهر لك سببه بوضوح هنا
        st.error(f"حدث خطأ: {e}")
