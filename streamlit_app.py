import streamlit as st
import requests

st.set_page_config(page_title="Prediction Chatbot", layout="centered")
st.markdown(
    "<h1 style='text-align: center;'>❤️ Cardiovascular Disease Prediction Chatbot 🤖</h1>",
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "message": "Hi! I'm CVD Prediction Bot. Say 'hi' or ask to check your heart health!"}
    ]
    st.session_state.state = "idle"
    st.session_state.inputs = {}
    st.session_state.feature_list = [
        ("age", "What is your age?"),
        ("sex", "What is your biological sex? (Type 'male' or 'female')"),
        ("cp", "Chest pain type (1-4)?"),
        ("trestbps", "Resting blood pressure?"),
        ("chol", "Serum cholesterol (mg/dl)?"),
        ("fbs", "Fasting blood sugar >120 mg/dl? (1=yes, 0=no)"),
        ("restecg", "Resting ECG (0=normal, 1=abnormal, 2=LVH)?"),
        ("thalach", "Maximum heart rate achieved?"),
        ("exang", "Exercise-induced angina? (1=yes, 0=no)"),
        ("oldpeak", "Oldpeak (ST depression)?"),
        ("slope", "Slope of peak exercise ST segment (1-3)?"),
        ("ca", "Number of major vessels colored by fluoroscopy (0-3)?"),
        ("thal", "Thalassemia (3=normal, 6=fixed, 7=reversible)?")
    ]
    st.session_state.current_feature = 0

def styled_message(msg, who="bot"):
    align = "right" if who == "user" else "left"
    color = "#e6f7ff" if who == "bot" else "#d5f5e3"
    avatar = "🤖" if who == "bot" else "🧑"
    st.markdown(
        f"<div style='display:flex; flex-direction:row; justify-content:{align};'>"
        f"<span style='background:{color}; border-radius:10px; padding:8px 16px; margin:3px; max-width:75%;"
        f"display:inline-block'><b>{avatar} {'Bot' if who=='bot' else 'You'}:</b> {msg}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

def bot_message(text):
    st.session_state.messages.append({"role": "bot", "message": text})

def user_message(text):
    st.session_state.messages.append({"role": "user", "message": text})

def process_user_message(user_msg):
    msg_lower = user_msg.lower()
    if st.session_state.state == "idle":
        if any(greet in msg_lower for greet in ["hi", "hello", "hey"]):
            bot_message("Hi there! Would you like to check your cardiovascular health? (Type 'yes' to start or ask directly)")
        elif any(term in msg_lower for term in ["check", "cardio", "heart"]):
            bot_message("Great! Let's begin your cardiovascular health check.")
            bot_message(st.session_state.feature_list[0][1])
            st.session_state.state = "collecting"
        elif "yes" in msg_lower:
            bot_message("Okay, let's start your health check.")
            bot_message(st.session_state.feature_list[0][1])
            st.session_state.state = "collecting"
        else:
            bot_message("You can greet me or directly ask to check your heart health.")
    elif st.session_state.state == "collecting":
        if msg_lower == "back" and st.session_state.current_feature > 0:
            st.session_state.current_feature -= 1
            last_key = st.session_state.feature_list[st.session_state.current_feature][0]
            if last_key in st.session_state.inputs:
                del st.session_state.inputs[last_key]
            bot_message(st.session_state.feature_list[st.session_state.current_feature][1])
        else:
            f_key, f_question = st.session_state.feature_list[st.session_state.current_feature]
            if f_key == "sex":
                if msg_lower in ["male", "m"]:
                    val = 1
                elif msg_lower in ["female", "f"]:
                    val = 0
                else:
                    bot_message('Please enter "male" or "female" for your sex (or type "back" to go to previous).')
                    return
            else:
                try:
                    val = float(user_msg)
                except Exception:
                    bot_message(f"Please enter a valid number for: {f_question} or type 'back' to go back.")
                    return
            st.session_state.inputs[f_key] = val
            st.session_state.current_feature += 1
            if st.session_state.current_feature < len(st.session_state.feature_list):
                bot_message(st.session_state.feature_list[st.session_state.current_feature][1])
            else:
                bot_message("Processing your results, please wait...")
                try:
                    api_url = "http://127.0.0.1:8000/predict"
                    resp = requests.post(api_url, json=st.session_state.inputs)
                    if resp.status_code == 200:
                        result = resp.json()
                        prob = result['probability']
                        pred = result['label']
                        if pred == 1:
                            bot_message(f"⚠️ High risk of heart disease! (Probability: {prob:.2f})\nType 'restart' to check again.")
                        else:
                            bot_message(f"✅ Low risk of heart disease. (Probability: {prob:.2f})\nType 'restart' to check again.")
                    else:
                        bot_message(f"API error {resp.status_code}: {resp.text}")
                except Exception as e:
                    bot_message(f"Failed to contact backend: {e}")
                st.session_state.state = "done"
    elif st.session_state.state == "done":
        if "restart" in msg_lower:
            st.session_state.state = "idle"
            st.session_state.inputs = {}
            st.session_state.current_feature = 0
            st.session_state.messages.append({"role": "bot", "message": "Let's start again! Greet me or ask to check your heart health."})
        else:
            bot_message("Type 'restart' to try again.")

for msg in st.session_state.messages:
    styled_message(msg["message"], who=msg["role"])

with st.form("input-form", clear_on_submit=True):
    user_input = st.text_input(
        "You:", key="user_input", label_visibility="collapsed",
        autocomplete="off",
        placeholder="Type your answer here and press Enter"
    )
    sent = st.form_submit_button("Send")
    if sent and user_input and user_input.strip():
        user_message(user_input)
        process_user_message(user_input)

st.info("Type 'back' to correct previous answer or 'restart' to try again. Say 'hi' to start.")
st.markdown("---\nThis chat assistant is for demo purposes only and does NOT provide medical advice.")
