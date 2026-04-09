import streamlit as st
import google.generativeai as genai

# 1. إعداد واجهة الموقع
st.set_page_config(page_title="TechSupport_DZ", page_icon="💻")
st.title("TechSupport_DZ 🛠️")
st.write("مرحباً بك، صف لي مشكلتك التقنية وسأساعدك فوراً.")

# 2. ربط الذكاء الاصطناعي (المفتاح الخاص بك)
genai.configure(api_key="AIzaSyCjh9vUSX0nQ2jvKU4sZ6UtqVlL6-HILtc")
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. التعليمات البرمجية (Prompt)
system_instruction = "أنت خبير صيانة ويندوز ولابتوب، اسمك TechSupport_DZ. تجيب بوضوح وباللغة العربية مع خطوات مرتبة."

# 4. إدارة سجل المحادثة (هذا الجزء كان ناقصاً عندك)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # إرسال التعليمات مع سؤال المستخدم في قائمة واحدة لتجنب أخطاء الدمج
    response = model.generate_content([system_instruction, prompt])
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
