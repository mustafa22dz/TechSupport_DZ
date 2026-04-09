import streamlit as st
import google.generativeai as genai

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="TechSupport_DZ",
    page_icon="🛠️",
    layout="centered"
)

st.title("TechSupport_DZ 🛠️")
st.caption("مساعد دعم فني لمشاكل ويندوز واللابتوب")

# =========================
# API KEY
# =========================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("❌ لم يتم العثور على GEMINI_API_KEY في Secrets")
    st.stop()

genai.configure(api_key=API_KEY)

# =========================
# MODEL FALLBACK SYSTEM
# =========================
AVAILABLE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]

def get_working_model():
    for model_name in AVAILABLE_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            test = model.generate_content("ping")
            if test:
                return model, model_name
        except Exception:
            continue
    return None, None

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    model, model_name = get_working_model()

    if model is None:
        st.error("❌ لم يتم العثور على أي موديل Gemini متاح لحسابك/API Key")
        st.stop()

    st.session_state.model = model
    st.session_state.model_name = model_name

# =========================
# SHOW ACTIVE MODEL
# =========================
st.success(f"✅ متصل بـ: {st.session_state.model_name}")

# =========================
# DISPLAY CHAT HISTORY
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# USER INPUT
# =========================
prompt = st.chat_input("كيف يمكنني مساعدتك؟")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # بناء history نصي
        history_text = ""
        for msg in st.session_state.messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"

        full_prompt = f"""
أنت خبير دعم فني للحواسيب ومشاكل ويندوز.

المحادثة السابقة:
{history_text}

أجب على آخر سؤال بشكل واضح ومفيد.
"""

        response = st.session_state.model.generate_content(full_prompt)
        reply = response.text

    except Exception as e:
        reply = f"❌ حدث خطأ أثناء توليد الرد:\n\n{str(e)}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with st.chat_message("assistant"):
        st.markdown(reply)
