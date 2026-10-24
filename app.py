import os
from pathlib import Path
import streamlit as st

# Ensure .env is read as local fallback
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            val = v.strip().strip("'\"")
            if val and not os.getenv(k.strip()):
                os.environ[k.strip()] = val

import sarvam_service

# Page Configuration
st.set_page_config(
    page_title="Aawaz se Diagnosis | JEE Physics",
    page_icon="🎙️",
    layout="wide",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .question-box {
        background-color: #F8FAFC;
        border-left: 5px solid #3B82F6;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        font-size: 1.05rem;
    }
    .auth-box {
        max-width: 420px;
        margin: 4rem auto;
        padding: 2rem;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 1. Password Protection (APP_PASSWORD)
def get_configured_password():
    try:
        if hasattr(st, "secrets") and "APP_PASSWORD" in st.secrets:
            return st.secrets["APP_PASSWORD"]
    except Exception:
        pass
    return os.getenv("APP_PASSWORD")

app_password = get_configured_password()

if app_password:
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.markdown(
            """
            <div class="auth-box">
                <h3 style="margin-top:0;">🔒 Access Protected</h3>
                <p style="color: #64748B;">Enter the access password to use <b>Aawaz se Diagnosis</b>.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            with st.form("login_form"):
                entered_pwd = st.text_input("Password", type="password", placeholder="Enter APP_PASSWORD")
                submit_btn = st.form_submit_button("Unlock App", use_container_width=True)
                if submit_btn:
                    if entered_pwd == app_password:
                        st.session_state["authenticated"] = True
                        st.rerun()
                    else:
                        st.error("Incorrect password. Please try again.")
            st.stop()

# 2. Check Sarvam API Key
try:
    sarvam_service.get_api_key()
except Exception:
    st.error("⚠️ `SARVAM_API_KEY` is not found. Please set it in Streamlit Cloud Secrets or in your local `.env` file.")
    st.stop()

# 3. Session Quota Limits
MAX_DIAGNOSES = 20
if "diagnosis_count" not in st.session_state:
    st.session_state["diagnosis_count"] = 0

# Sidebar with Quota and Controls
with st.sidebar:
    st.title("⚙️ Session Controls")
    st.metric("Diagnoses Used", f"{st.session_state['diagnosis_count']} / {MAX_DIAGNOSES}")
    quota_pct = min(st.session_state["diagnosis_count"] / MAX_DIAGNOSES, 1.0)
    st.progress(quota_pct)
    st.caption(f"Each session allows up to {MAX_DIAGNOSES} diagnoses to preserve Sarvam AI credits.")
    
    st.divider()
    speaker = st.selectbox(
        "Tutor Voice (Bulbul v3)",
        options=["aditya", "ritu", "priya", "rahul", "kavya", "ishita", "rohan"],
        index=0,
        help="Select voice persona for the spoken audio re-teaching.",
    )
    st.divider()
    st.caption("Powered by **Sarvam AI**: `saaras:v3`, `sarvam-105b`, `bulbul:v3`")

st.markdown('<div class="main-header">🎙️ Aawaz se Diagnosis</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Spoken Misconception Detector for JEE Physics Students &bull; Powered by <b>Sarvam AI</b> (<code>sarvam-105b</code>, <code>saaras:v3</code>, <code>bulbul:v3</code>)</div>',
    unsafe_allow_html=True,
)

# Kinematics Questions
QUESTIONS = [
    {
        "id": "q1",
        "title": "Question 1: Ball at Maximum Height",
        "question": "A ball is thrown straight upwards into the air. At the exact highest point of its trajectory, what are its velocity and its acceleration? Explain the physics reason behind both.",
        "trap": "Common JEE Trap: Confusing instantaneous zero velocity with zero acceleration.",
    },
    {
        "id": "q2",
        "title": "Question 2: Constant Speed with Acceleration",
        "question": "Can an object have a constant speed and yet possess a non-zero acceleration at the same time? Explain why or why not, and give an example.",
        "trap": "Common JEE Trap: Believing acceleration is only rate of change of speed, ignoring velocity's directional vector.",
    },
    {
        "id": "q3",
        "title": "Question 3: Vacuum Free Fall (Feather vs Heavy Ball)",
        "question": "A 10 kg iron sphere and a 5-gram feather are dropped simultaneously from a height of 20 meters inside an evacuated vacuum chamber. Which one reaches the ground first, and why?",
        "trap": "Common JEE Trap: Thinking heavier objects accelerate faster due to greater gravitational force, neglecting proportional inertia.",
    },
]

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("1. Select Kinematics Question")
    question_titles = [q["title"] for q in QUESTIONS]
    selected_idx = st.selectbox("Choose a question to explain:", range(len(QUESTIONS)), format_func=lambda i: question_titles[i])
    current_q = QUESTIONS[selected_idx]

    st.markdown(
        f"""
        <div class="question-box">
            <b>{current_q["title"]}</b><br/><br/>
            {current_q["question"]}
            <br/><br/>
            <small style="color: #64748B;">💡 <i>{current_q["trap"]}</i></small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("2. Record Your Spoken Explanation")
    st.caption("Speak your answer clearly in English into your microphone.")
    audio_data = st.audio_input("Record your voice")

with col2:
    st.subheader("Diagnosis & Voice Feedback")

    if audio_data is None:
        st.info("🎙️ Waiting for your recording. Click the mic icon on the left, speak your reasoning, and stop when finished.")
    else:
        audio_bytes = audio_data.getvalue()
        audio_hash = f"{current_q['id']}_{hash(audio_bytes)}_{speaker}"

        # Check if already processed in session
        if st.session_state.get("processed_audio_hash") != audio_hash:
            # Check session quota before calling APIs
            if st.session_state["diagnosis_count"] >= MAX_DIAGNOSES:
                st.error(f"🛑 You have reached the session limit of {MAX_DIAGNOSES} diagnoses. Please restart your session if needed.")
                st.stop()

            with st.spinner("Step 1/3: Transcribing your voice using Saaras v3..."):
                try:
                    transcript = sarvam_service.transcribe_audio(audio_bytes)
                except Exception as e:
                    st.error(f"❌ Error in Speech-to-Text (saaras:v3): {e}")
                    st.stop()

            if not transcript:
                st.warning("⚠️ No audible speech could be detected in the recording. Please try recording again speaking closer to the microphone.")
                st.stop()

            with st.spinner("Step 2/3: Diagnosing physics misconceptions using Sarvam-105B..."):
                try:
                    diagnosis = sarvam_service.diagnose_misconception(current_q["question"], transcript)
                except Exception as e:
                    st.error(f"❌ Error in Misconception Diagnosis (sarvam-105b): {e}")
                    st.stop()

            re_teaching_text = diagnosis.get("re_teaching", "")
            tts_audio = None
            if re_teaching_text:
                with st.spinner("Step 3/3: Synthesizing tutor voice explanation using Bulbul v3..."):
                    try:
                        tts_audio = sarvam_service.generate_speech(re_teaching_text, speaker=speaker)
                    except Exception as e:
                        st.error(f"❌ Error in Text-to-Speech (bulbul:v3): {e}")

            # Increment quota count and store results in session state
            st.session_state["diagnosis_count"] += 1
            st.session_state["processed_audio_hash"] = audio_hash
            st.session_state["transcript"] = transcript
            st.session_state["diagnosis"] = diagnosis
            st.session_state["tts_audio"] = tts_audio

        # Display cached results from session state
        transcript = st.session_state.get("transcript", "")
        diagnosis = st.session_state.get("diagnosis", {})
        tts_audio = st.session_state.get("tts_audio")

        # 1. Transcript Display
        st.markdown("#### 📝 Your Spoken Transcript (`saaras:v3`)")
        st.write(f'"{transcript}"')

        # 2. Diagnosis Display
        st.markdown("#### 🧠 Misconception Diagnosis (`sarvam-105b`)")
        is_correct = diagnosis.get("is_correct", False)
        misconception_name = diagnosis.get("misconception_name", "None")
        explanation = diagnosis.get("explanation_of_mistake", "")
        re_teaching = diagnosis.get("re_teaching", "")

        if is_correct:
            st.success(f"✅ **Conceptually Correct!** (Misconception: {misconception_name})")
        else:
            st.error(f"❌ **Misconception Identified:** {misconception_name}")

        st.markdown(f"**Analysis of Reasoning:**\n\n{explanation}")

        # 3. Analogy Re-teaching & Bulbul Audio
        st.markdown("#### 💡 Intuitive Analogy & Re-teaching")
        st.info(re_teaching)

        if tts_audio:
            st.markdown("#### 🔊 Listen to Tutor Explanation (`bulbul:v3`)")
            st.audio(tts_audio, format="audio/wav")
