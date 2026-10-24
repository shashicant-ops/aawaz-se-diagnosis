# 🎙️ Aawaz se Diagnosis

> **Spoken Misconception Detector for JEE Physics Students**  
> *Powered by Sarvam AI (`saaras:v3`, `sarvam-105b`, `bulbul:v3`) and Streamlit.*

---

## 💡 The Problem & Idea

In competitive exams like JEE Advanced, physics questions are designed to exploit subtle conceptual misconceptions. Standard multiple-choice tests fail to diagnose *why* a student arrived at an answer. 

**Aawaz se Diagnosis** lets students speak their raw conceptual reasoning aloud in their own voice. The AI listens, diagnoses the exact physics flaw in their mental model, and responds with a memorable real-world analogy read out loud by a voice tutor.

---

## 🤖 Sarvam AI Models Used

| Stage | Model | Role & Implementation |
|---|---|---|
| **1. Speech-to-Text** | `saaras:v3` | Transcribes the student's spoken audio (recorded via Streamlit) into clean English text, optimized for Indian accents and classroom vocabulary. |
| **2. Reasoning & Diagnosis** | `sarvam-105b` | Analyzes the transcript against the kinematics problem. Evaluates whether the logic is sound or falls into classic JEE traps (e.g. $v=0 \implies a=0$, constant speed $\implies a=0$, heavier falls faster in vacuum). Returns strictly structured JSON: `is_correct`, `misconception_name`, `explanation_of_mistake`, and `re_teaching`. |
| **3. Voice Tutor Synthesis** | `bulbul:v3` | Takes the generated real-world analogy and synthesizes natural, expressive spoken audio tutor feedback using personas such as `aditya`, `ritu`, and `priya`. |

---

## 🔒 Security & Credit Protection

To safely deploy on public hosting platforms like **Streamlit Community Cloud**:
- **API Key Precedence**: Reads `SARVAM_API_KEY` from `st.secrets` first, falling back to local `.env`. Keys are never exposed or committed.
- **Access Password Protection**: Optional `APP_PASSWORD` can be set in secrets. Unauthenticated users cannot view questions or make API calls.
- **Session Quota Limits**: Capped at **20 diagnoses per session** to prevent automated or abusive credit exhaustion.

---

## 🚀 How to Run Locally

### 1. Prerequisites
- Python 3.9+
- A Sarvam AI API subscription key from [Sarvam AI Developer Portal](https://docs.sarvam.ai)

### 2. Install Dependencies
```bash
git clone <your-repo-url>
cd aawaz
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the root directory:
```env
SARVAM_API_KEY=your_actual_sarvam_api_key_here
# Optional password protection:
APP_PASSWORD=your_optional_password
```
*(Note: `.env` is already included in `.gitignore` and must never be committed).*

### 4. Run the Streamlit App
```bash
streamlit run app.py
```
Open **http://localhost:8501** in your browser.

---

## ☁️ Deploying to Streamlit Community Cloud

1. Push this repository to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```
2. Log in to [share.streamlit.io](https://share.streamlit.io/) and create a **New app**.
3. Select your repository, branch (`main`), and main file path (`app.py`).
4. Click **Advanced settings...** > **Secrets** and paste:
   ```toml
   SARVAM_API_KEY = "your_sarvam_api_key_here"
   APP_PASSWORD = "choose_a_password_for_users"
   ```
5. Click **Deploy!**

---

## 📁 Project Structure

```text
aawaz/
├── app.py               # Streamlit application UI, auth & session quota logic
├── sarvam_service.py    # Wrapper functions for Saaras, Sarvam-105B & Bulbul
├── requirements.txt     # Python dependencies (streamlit, sarvamai)
├── .gitignore           # Excludes .env, secrets, and caches
├── .env                 # Local environment file (ignored by git)
└── README.md            # Project overview and setup instructions
```
