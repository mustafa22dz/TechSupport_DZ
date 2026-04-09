import streamlit as st
import google.generativeai as genai

# إعداد واجهة الموقع
st.set_page_config(page_title="TechSupport_DZ", page_icon="💻")
st.title("TechSupport_DZ 🛠️")
st.write("مرحباً بك، صف لي مشكلتك التقنية وسأساعدك فوراً.")

# ربط الذكاء الاصطناعي (ضع مفتاحك هنا)
genai.configure(api_key="AIzaSyCjh9vUSX0nQ2jvKU4sZ6UtqVlL6-HILtc")
model = genai.GenerativeModel('gemini-1.5-flash')

# التعليمات البرمجية (Prompt)
system_instruction = "أنت خبير صيانة ويندوز ولابتوب... (ضع النص الكامل هنا)"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = model.generate_content(system_instruction + prompt)
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
