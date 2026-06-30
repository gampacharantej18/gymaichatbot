import asyncio
import sys

# ✅ Fix Windows event loop issue
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st
from langchain_mistralai import ChatMistralAI
import os

# ✅ Initialize the model safely
model = ChatMistralAI(
    model="mistral-large-latest",
    api_key=os.getenv("MISTRAL_API_KEY"),
    system_message="You are an AI Gym Trainer. Always give safe, personalized advice about fitness, nutrition, and workouts."
)

# 🎨 Professional theme setup
st.set_page_config(
    page_title="AI Gym Trainer",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 🧍 User profile setup
def user_profile():
    st.sidebar.title("🏋️ User Profile")
    st.sidebar.info("Fill in your details for a personalized fitness plan:")

    name = st.sidebar.text_input("Name")
    age = st.sidebar.number_input("Age", min_value=10, max_value=100, step=1)
    gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, step=1)
    weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, step=1)
    goal = st.sidebar.selectbox(
        "Fitness Goal",
        [
            "Lose Weight",
            "Gain Muscle (Bulk Up)",
            "Get Shredded",
            "Improve Endurance",
            "General Fitness",
            "Custom Goal"
        ]
    )

    custom_goal = ""
    if goal == "Custom Goal":
        custom_goal = st.sidebar.text_input("Describe your specific goal")

    if st.sidebar.button("Generate Plan"):
        user_data = {
            "name": name,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "goal": custom_goal if custom_goal else goal
        }
        st.session_state.user_data = user_data
        st.session_state.messages = []
        st.success("✅ Profile saved! You can now chat with your AI Trainer.")

# 💬 Chat interface
def chat_interface(model):
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>💬 Chat with your AI Gym Trainer</h1>", unsafe_allow_html=True)
    st.write("Ask me anything about fitness, nutrition, or your workout plan!")

    if "user_data" not in st.session_state:
        st.warning("Please fill out your profile in the sidebar first.")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new user input
    if prompt := st.chat_input("What would you like to know?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing your profile and goal..."):
                user_info = st.session_state.user_data
                context = (
                    f"User details:\n"
                    f"Name: {user_info['name']}\n"
                    f"Age: {user_info['age']}\n"
                    f"Gender: {user_info['gender']}\n"
                    f"Height: {user_info['height']} cm\n"
                    f"Weight: {user_info['weight']} kg\n"
                    f"Goal: {user_info['goal']}\n\n"
                    f"User question: {prompt}"
                )
                full_response = model.invoke(context)
                st.markdown(f"### 📝 Personalized Plan\n{full_response.content}")
            st.session_state.messages.append({"role": "assistant", "content": full_response.content})

# 🚀 Run the app
if __name__ == "__main__":
    user_profile()
    chat_interface(model)
