import streamlit as st
from langchain_mistralai import ChatMistralAI
import os
from dotenv import load_dotenv

load_dotenv()  



st.set_page_config(
    page_title="AI Gym Trainer",
    page_icon="assets/logo.png",  
    layout="wide",
    initial_sidebar_state="collapsed",
)




st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&display=swap');

/* ── Root palette ── */
:root {
    --gold:      #C9A84C;
    --gold-dim:  #9A7A2E;
    --dark-bg:   #0D0D0D;
    --card-bg:   #161616;
    --border:    #2A2A2A;
    --text-main: #E8E3D8;
    --text-mute: #7A7570;
    --accent:    #C9A84C;
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--dark-bg) !important;
    color: var(--text-main);
    font-family: 'Source Sans 3', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ── Hide Streamlit default branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--dark-bg); }
::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 3px; }

/* ── Top banner ── */
.trainer-header {
    text-align: center;
    padding: 2.8rem 1rem 1.4rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.trainer-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    color: var(--gold);
    letter-spacing: 0.04em;
    margin: 0 0 0.3rem;
}
.trainer-header p {
    font-size: 1rem;
    color: var(--text-mute);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 0;
}
.gold-rule {
    width: 60px;
    height: 2px;
    background: var(--gold);
    margin: 0.8rem auto 0;
    border-radius: 1px;
}

/* ── Card wrapper ── */
.profile-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem 2.2rem;
    max-width: 700px;
    margin: 0 auto 2rem;
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
}
.profile-card h3 {
    font-family: 'Playfair Display', serif;
    color: var(--gold);
    font-size: 1.35rem;
    margin-bottom: 0.3rem;
}
.step-label {
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-mute);
    margin-bottom: 1.4rem;
}
.step-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.4rem 0;
}

/* ── Form inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextArea"] textarea {
    background-color: #1E1E1E !important;
    border: 1px solid var(--border) !important;
    color: var(--text-main) !important;
    border-radius: 6px !important;
    font-family: 'Source Sans 3', sans-serif !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.18) !important;
}
label, .stSelectbox label, .stNumberInput label {
    color: var(--text-mute) !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-family: 'Source Sans 3', sans-serif !important;
}

/* ── Radio buttons (goal selection) ── */
[data-testid="stRadio"] label {
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-size: 0.95rem !important;
    color: var(--text-main) !important;
}
[data-testid="stRadio"] > div {
    gap: 0.5rem;
}

/* ── Primary button ── */
.stButton > button {
    background: linear-gradient(135deg, var(--gold), var(--gold-dim)) !important;
    color: #0D0D0D !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.65rem 2.2rem !important;
    transition: opacity 0.2s ease, transform 0.15s ease !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    margin-bottom: 0.8rem !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stChatMessage"][data-testid*="user"] {
    border-left: 3px solid var(--gold) !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] td {
    color: var(--text-main) !important;
    font-size: 0.97rem !important;
    line-height: 1.75 !important;
}
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 {
    color: var(--gold) !important;
    font-family: 'Playfair Display', serif !important;
}
[data-testid="stChatMessage"] strong { color: var(--gold) !important; }
[data-testid="stChatMessage"] code {
    background: #1E1E1E !important;
    color: var(--gold) !important;
    border-radius: 4px !important;
    padding: 0.1em 0.4em !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--text-main) !important;
    font-family: 'Source Sans 3', sans-serif !important;
}

/* ── Profile summary badge ── */
.profile-badge {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-left: 3px solid var(--gold);
    border-radius: 8px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 1.2rem;
    font-size: 0.83rem;
    color: var(--text-mute);
    letter-spacing: 0.04em;
}
.profile-badge span { color: var(--text-main); font-weight: 600; }

/* ── Section heading in chat area ── */
.chat-section-title {
    font-family: 'Playfair Display', serif;
    color: var(--gold);
    font-size: 1.15rem;
    margin: 0 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

/* ── Spinner text ── */
[data-testid="stSpinner"] p { color: var(--text-mute) !important; }

/* ── Progress / step indicator ── */
.step-indicator {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    margin-bottom: 1.5rem;
}
.step-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--border);
}
.step-dot.active { background: var(--gold); }
</style>
""", unsafe_allow_html=True)



st.markdown("""
<div class="trainer-header">
    <h1>AI Gym Trainer</h1>
    <p>Personalised Fitness & Nutrition Intelligence</p>
    <div class="gold-rule"></div>
</div>
""", unsafe_allow_html=True)


for key, default in {
    "step": 1,         
    "profile": {},
    "goal": "",
    "messages": [],
    "plan_generated": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def build_system_prompt(profile: dict, goal: str) -> str:
    p = profile
    bmi = round(p["weight_kg"] / ((p["height_cm"] / 100) ** 2), 1)
    bmi_category = (
        "Underweight" if bmi < 18.5 else
        "Normal weight" if bmi < 25 else
        "Overweight" if bmi < 30 else
        "Obese"
    )
    return f"""You are an elite personal trainer and certified nutritionist.

CLIENT PROFILE:
- Name        : {p.get('name', 'Client')}
- Age         : {p['age']} years
- Gender      : {p['gender']}
- Height      : {p['height_cm']} cm
- Weight      : {p['weight_kg']} kg
- BMI         : {bmi} ({bmi_category})
- Activity    : {p['activity_level']}
- Experience  : {p['experience']}
- Injuries    : {p.get('injuries', 'None reported')}

CLIENT GOAL:
{goal}

YOUR RESPONSIBILITIES:
1. Provide a detailed, structured fitness and nutrition plan tailored exactly to the client profile and goal above.
2. Use professional, motivating language — classic and authoritative, never casual or generic.
3. For the initial plan, structure your response with clear sections:
   - Brief Analysis (BMI, fitness baseline)
   - Weekly Workout Schedule (days, exercises, sets, reps)
   - Nutrition Guidelines (daily calories, macros, meal timing)
   - Supplement Recommendations (only evidence-based)
   - Recovery & Lifestyle Tips
4. For follow-up questions, answer precisely and incorporate the client's profile in every recommendation.
5. Always use markdown formatting: bold section headers, bullet points, tables where appropriate.
"""



def step_indicator(current: int):
    dots = "".join(
        f'<div class="step-dot{"  active" if i == current else ""}"></div>'
        for i in range(1, 4)
    )
    st.markdown(f'<div class="step-indicator">{dots}</div>', unsafe_allow_html=True)



def render_profile_form():
    step_indicator(1)
    st.markdown("""
    <div class="profile-card">
        <h3>Your Personal Profile</h3>
        <div class="step-label">Step 1 of 2 — Physical Details</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name", placeholder="John Smith")
            age = st.number_input("Age (years)", min_value=13, max_value=90, value=25)
            height_cm = st.number_input("Height (cm)", min_value=100, max_value=250, value=175)
            weight_kg = st.number_input("Weight (kg)", min_value=30, max_value=300, value=75)

        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])
            activity_level = st.selectbox(
                "Current Activity Level",
                [
                    "Sedentary (desk job, no exercise)",
                    "Lightly active (1-2 days/week)",
                    "Moderately active (3-4 days/week)",
                    "Very active (5-6 days/week)",
                    "Athlete (2x daily / intense training)",
                ],
            )
            experience = st.selectbox(
                "Gym Experience",
                ["Beginner (0-6 months)", "Intermediate (6 months - 2 years)", "Advanced (2+ years)"],
            )
            injuries = st.text_input(
                "Injuries / Health Conditions",
                placeholder="e.g. lower back pain, knee issues — or leave blank",
            )

        st.markdown("<hr class='step-divider'>", unsafe_allow_html=True)
        col_btn, _ = st.columns([1, 3])
        with col_btn:
            if st.button("Continue to Goals"):
                if not name.strip():
                    st.warning("Please enter your name to continue.")
                else:
                    st.session_state.profile = {
                        "name": name.strip(),
                        "age": age,
                        "gender": gender,
                        "height_cm": height_cm,
                        "weight_kg": weight_kg,
                        "activity_level": activity_level,
                        "experience": experience,
                        "injuries": injuries.strip() or "None reported",
                    }
                    st.session_state.step = 2
                    st.rerun()



def render_goal_form():
    step_indicator(2)
    p = st.session_state.profile
    st.markdown(f"""
    <div class="profile-card">
        <h3>Define Your Goal, {p['name'].split()[0]}</h3>
        <div class="step-label">Step 2 of 2 — Training Objective</div>
    </div>
    """, unsafe_allow_html=True)

    preset_goals = [
        "Lose weight and reduce body fat",
        "Build muscle and increase size (Bulk)",
        "Get lean and shredded (cut body fat, maintain muscle)",
        "Improve overall fitness and endurance",
        "Increase strength and power",
        "Athletic performance and sport-specific training",
        "Rehabilitation and injury recovery",
        "Custom goal (describe below)",
    ]

    selected_preset = st.radio("Select your primary goal", preset_goals)

    custom_goal = ""
    if selected_preset == "Custom goal (describe below)":
        custom_goal = st.text_area(
            "Describe your specific goal in detail",
            placeholder="e.g. I want to train for a marathon while maintaining muscle mass...",
            height=100,
        )

    additional = st.text_area(
        "Any additional context or preferences? (optional)",
        placeholder="e.g. I prefer morning workouts, no gym access on weekends, vegetarian diet...",
        height=80,
    )

    st.markdown("<hr class='step-divider'>", unsafe_allow_html=True)
    col_back, col_btn, _ = st.columns([1, 1.5, 3])
    with col_back:
        if st.button("Back"):
            st.session_state.step = 1
            st.rerun()
    with col_btn:
        if st.button("Generate My Plan"):
            goal_text = custom_goal.strip() if selected_preset == "Custom goal (describe below)" else selected_preset
            if selected_preset == "Custom goal (describe below)" and not goal_text:
                st.warning("Please describe your custom goal.")
            else:
                full_goal = goal_text
                if additional.strip():
                    full_goal += f"\n\nAdditional preferences: {additional.strip()}"
                st.session_state.goal = full_goal
                st.session_state.step = 3
                st.session_state.plan_generated = False
                st.rerun()



def render_chat(model):
    p = st.session_state.profile
    bmi = round(p["weight_kg"] / ((p["height_cm"] / 100) ** 2), 1)

    st.markdown(f"""
    <div class="profile-badge">
        <strong style="color: var(--gold); letter-spacing: 0.08em; text-transform: uppercase; font-size: 0.75rem;">
            Active Profile
        </strong><br>
        <span>{p['name']}</span> &nbsp;|&nbsp;
        {p['age']} yrs &nbsp;|&nbsp;
        {p['gender']} &nbsp;|&nbsp;
        {p['height_cm']} cm &nbsp;|&nbsp;
        {p['weight_kg']} kg &nbsp;|&nbsp;
        BMI <span>{bmi}</span> &nbsp;|&nbsp;
        {p['experience']}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="chat-section-title">Your Personalised Training Session</p>', unsafe_allow_html=True)

   
    if not st.session_state.plan_generated:
        system_prompt = build_system_prompt(p, st.session_state.goal)
        initial_prompt = (
            f"Please analyse my profile thoroughly and provide my complete, structured fitness and nutrition plan "
            f"based on my goal: {st.session_state.goal}"
        )
        st.session_state.messages = []

        with st.chat_message("assistant"):
            with st.spinner("Analysing your profile and generating your plan..."):
                from langchain_core.messages import SystemMessage, HumanMessage
                response = model.invoke([
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=initial_prompt),
                ])
                st.markdown(response.content)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response.content,
            "_system": system_prompt,
        })
        st.session_state.plan_generated = True

    
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(msg["content"])
        elif msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])

    
    if user_input := st.chat_input("Ask a follow-up question about your plan..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

                system_prompt = build_system_prompt(p, st.session_state.goal)
                history = [SystemMessage(content=system_prompt)]

                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        history.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        history.append(AIMessage(content=msg["content"]))

                response = model.invoke(history)
                st.markdown(response.content)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response.content,
        })

    
    st.markdown("<br>", unsafe_allow_html=True)
    col_reset, _ = st.columns([1, 5])
    with col_reset:
        if st.button("Start Over"):
            for key in ["step", "profile", "goal", "messages", "plan_generated"]:
                del st.session_state[key]
            st.rerun()



def chat_interface(model):
    if st.session_state.step == 1:
        render_profile_form()
    elif st.session_state.step == 2:
        render_goal_form()
    elif st.session_state.step == 3:
        render_chat(model)



if __name__ == "__main__":
    api_key = os.getenv("MISTRAL_API_KEY", "")
    model = ChatMistralAI(
        model="mistral-large-latest",
        mistral_api_key=api_key,
        temperature=0.6,
    )
    chat_interface(model)
