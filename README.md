# Code Review Assistant ✨

A Flask-based web application that leverages the Grok AI model (via LangChain and Groq API) to provide detailed code reviews and interactive Q&A functionality. This tool allows developers to submit code snippets, receive professional feedback, ask follow-up questions, and maintain a history of reviews and conversations, all stored in a SQLite database. 🚀

---

## Features 🌟

- **Code Review** 🖥️: Submit code snippets and receive detailed feedback on quality, bugs, performance, security, and improvement suggestions.
- **Interactive Q&A** ❓: Ask follow-up questions about reviews with context-aware responses.
- **Conversation History** 📜: Persistent storage of reviews and conversations using SQLite.
- **Memory Management** 🧠: Maintains conversation context for each review session (up to 5 previous interactions).
- **RESTful API** 🌐: Simple endpoints for submitting code, asking questions, retrieving history, and deleting reviews.
- **Frontend Integration** 🎨: Basic HTML template (`index.html`) for user interaction.

---

## Tech Stack 🛠️

- **Backend:** Flask (Python) 🐍
- **AI Model:** Grok (via LangChain and Groq API) 🤖
- **Database:** SQLite 🗄️
- **Environment Management:** `python-dotenv` for API key handling 🔑
- **Dependencies:** Managed via `requirements.txt` 📦

---

## Prerequisites ✅

Before running the application, ensure you have the following installed:

- Python 3.8+ 🐍
- Git 🌿
- A Groq API key (sign up at [Groq](https://groq.com) to obtain one) 🔐

---

## Installation ⚙️

Follow these steps to set up the project locally:

1. **Clone the Repository** 📥
   ```bash
   git clone https://github.com/username/code-review-assistant.git
   cd code-review-assistant


## Create a Virtual Environment 🌀

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## Install Dependencies 📦

pip install -r requirements.txt


## Set Up Environment Variables 🔧

Create a .env file in the root directory.

Add your Groq API key:

GROQ_API_KEY=your_groq_api_key_here

## Initialize the Database 🗃️

The database (reviews.db) will be automatically created when you run the app for the first time.

## Run the Application 🚀

python app.py

The app will start in debug mode at http://127.0.0.1:5000

## Project Structure 📂

code-review-assistant/
├── app.py              # Main Flask application 🖥️

├── database.py         # Database initialization and operations 🗄️

├── requirements.txt    # Project dependencies 📦

├── templates/          # Frontend templates 🎨

│   └── index.html      # Home page template 🏠

├── .env                # Environment variables (not tracked) 🔑

└── reviews.db          # SQLite database (generated on first run) 🗃️


## Contact Information 📞

For any questions or feedback, feel free to reach out:

- **Email**: [ferasalshash@gmail.com](mailto:ferasalshash@gmail.com)  
- **GitHub**: [FerasAlshash](https://github.com/FerasAlshash)  
- **LinkedIn**: [Feras Alshash](https://www.linkedin.com/in/feras-alshash-bb3106a9/)  
