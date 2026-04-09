import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="TechSupport_DZ", page_icon="💻")
st.title("TechSupport_DZ 🛠️")

# ربط الـ API
genai.configure(api_key="AIzaSyCjh9vUSX0nQ2jvKU4sZ6UtqVlL6-HILtc")

# اختيار الموديل باسمه المباشر (هذا الاسم تقبله كل النسخ)
model = genai.GenerativeModel('models/gemini-1.5-flash')

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
        # إرسال النص مباشرة
        response = model.generate_content(f"أنت خبير صيانة ويندوز جزائري ذكي. أجب على هذا السؤال: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
