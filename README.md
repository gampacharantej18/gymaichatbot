# AI Gym Trainer Chatbot

This project provides an AI-powered Gym Trainer Chatbot built with Streamlit, LangChain, and MistralAI. It allows users to generate personalized workout plans based on their fitness goals, available equipment, duration, difficulty, and focus areas. Additionally, it includes a chatbot interface for general fitness and nutrition queries.

## Features

- **Personalized Workout Plan Generation**: Input your fitness preferences and get a tailored workout routine.
- **Interactive Chatbot**: Ask fitness-related questions and receive AI-powered responses.
- **Streamlit UI/UX**: A clean and intuitive user interface for easy interaction.

## Project Structure

```
GenAI-GymTrainer-1/
├── app.py
├── chatbot.py
├── .env
├── requirements.txt
├── .gitignore
└── README.md
```

- `app.py`: The main Streamlit application that handles workout plan generation and integrates the chatbot.
- `chatbot.py`: Contains the logic for the interactive fitness chatbot.
- `.env`: Stores your MistralAI API key (not committed to version control).
- `requirements.txt`: Lists all Python dependencies required to run the application.
- `.gitignore`: Specifies intentionally untracked files to ignore.
- `README.md`: This file, providing an overview and instructions.

## Setup and Installation

Follow these steps to set up and run the AI Gym Trainer Chatbot locally:

### 1. Clone the Repository (if applicable)

If you received this project as a ZIP file, extract it. Otherwise, if it's in a repository, clone it:

```bash
git clone <repository_url>
cd GenAI-GymTrainer-1
```

### 2. Create a Virtual Environment (Recommended)

It's good practice to use a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Configure MistralAI API Key

Create a `.env` file in the root directory of the project (`GenAI-GymTrainer-1/`) and add your MistralAI API key:

```
MISTRAL_API_KEY="your_mistral_api_key_here"
```

Replace `your_mistral_api_key_here` with your actual MistralAI API key. You can obtain one from the [Mistral AI website](https://mistral.ai/).

### 5. Run the Streamlit Application

Once the setup is complete, run the Streamlit application:

```bash
streamlit run app.py
```

This will open the application in your web browser. If it doesn't open automatically, navigate to `http://localhost:8501`.

## Usage

### Workout Plan Generation

1. **Adjust Settings**: Use the sidebar on the left to select your fitness goal, available equipment, workout duration, difficulty level, and specific focus area.
2. **Generate Plan**: Click the "🚀 Generate Workout Plan" button.
3. **View Plan**: Your personalized workout plan will be displayed in the main section of the app.
4. **New Plan**: Click "🔄 Generate New Plan" to clear the current plan and generate a new one.

### Chatbot

Below the workout plan section, you'll find the chatbot interface:

1. **Ask Questions**: Type your fitness, nutrition, or workout-related questions into the chat input box.
2. **Get Answers**: The AI Gym Trainer will provide responses to your queries.

Enjoy your personalized AI Gym Trainer experience!
