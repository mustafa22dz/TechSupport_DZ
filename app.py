import streamlit as st
import google.generativeai as genai

# إعداد واجهة الموقع
st.set_page_config(page_title="TechSupport_DZ", page_icon="💻")
st.title("TechSupport_DZ 🛠️")
st.write("مرحباً بك في منصة الدعم الفني الذكي.")

# ربط الذكاء الاصطناعي
genai.configure(api_key="AIzaSyCjh9vUSX0nQ2jvKU4sZ6UtqVlL6-HILtc")

# محاولة اختيار أفضل محرك متاح لتجنب خطأ 404
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro') # محرك احتياطي قديم ومستقر جداً

system_instruction = "أنت خبير صيانة ويندوز، اسمك TechSupport_DZ. تجيب بالعربية وبخطوات مرتبة."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # إرسال الطلب بطريقة مبسطة جداً
        chat = model.start_chat(history=[])
        response = chat.send_message(f"{system_instruction}\n\nسؤال المستخدم: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"عذراً، حدث خطأ تقني: {e}")
