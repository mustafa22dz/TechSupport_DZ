import streamlit as st
from openai import OpenAI

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="TechSupport_DZ",
    page_icon="🛠️",
    layout="centered"
)

st.title("TechSupport_DZ 🛠️")
st.caption("مساعد دعم فني لمشاكل ويندوز واللابتوب (المزود السريع)")

# =========================
# API KEY & BASE URL
# =========================
# ملاحظة: يفضل وضع هذه القيم في Secrets لاحقاً، لكن سنضعها هنا لتعمل فوراً
API_KEY = "sk-Nm3CRnIJjnHgBc8U9lHgN6ZSGU7UXPh3ROLrlPbAvy6N77AS"
BASE_URL = "https://api.souimagery.fun/v1"

# إعداد العميل (Client)
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# =========================
# SESSION STATE (إدارة المحادثة)
# =========================
if "messages" not in st.session_state:
    # نضع تعليمات النظام كأول رسالة مخفية
    st.session_state.messages = [
        {"role": "system", "content": "أنت خبير دعم فني للحواسيب ومشاكل ويندوز، اسمك TechSupport_DZ. أجب بوضوح وباللغة العربية مع خطوات مرتبة."}
    ]

# =========================
# DISPLAY CHAT HISTORY
# =========================
# نعرض الرسائل ما عدا رسالة الـ system
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# =========================
# USER INPUT & RESPONSE
# =========================
prompt = st.chat_input("كيف يمكنني مساعدتك؟")

if prompt:
    # إضافة سؤال المستخدم للسجل وعرضه
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # طلب الرد من الموديل
        # ملاحظة: يمكنك تجربة "gpt-3.5-turbo" أو "gpt-4" أو "gemini-pro" حسب المتاح في souimagery
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=st.session_state.messages,
            temperature=0.7
        )
        
        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"❌ حدث خطأ في الاتصال بالمزود:\n\n{str(e)}"

    # إضافة رد البوت للسجل وعرضه
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
