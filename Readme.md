# 🍽️ GenAI Calorie Tracker

## 📖 Project Overview
The **GenAI Calorie Tracker** is an intelligent assistant that helps users monitor their daily food intake, estimate calories, and receive personalized diet suggestions.  
This project integrates **Generative AI (Gemini API)** with a backend calorie tracking system, enabling smart queries like:
- “How many calories are in 2 bananas and a glass of milk?”
- “Suggest a 2000-calorie vegetarian meal plan for today.”
- “Give me a zero-carb dinner recipe.”

The project also demonstrates advanced **prompt engineering techniques** like:
- Zero-Shot Prompting  
- Dynamic Prompting  
- Tokens & Tokenization Logging  
- Sampling Techniques (Temperature, Top-P, Top-K)

---

## 🎯 Features
- 🥗 **Food Logging** – Track calories based on food inputs.  
- 🧠 **GenAI Bot** – Query the model for summaries, recipes, or personalized diet advice.  
- 🔑 **Environment Config** – API keys secured using `.env`.  
- 🛠️ **Prompt Engineering** – Zero-Shot, Dynamic Prompting, Temperature, Top-P, and Top-K implemented.  
- 📊 **Token Logging** – Monitor tokens used in each request.  
- ☁️ **Scalable Backend** – Built to handle large requests and user traffic.  

---

## ⚙️ Tech Stack
- **Python 3.13+**
- **Google Gemini API** (`google-generativeai`)
- **dotenv** for environment variables
- **Git & GitHub** for version control
- **Prompt Engineering** concepts

---

## 🏗️ Implementation

### 1. **Backend**
- The backend uses Python to connect with the Gemini API.
- API key is securely stored in `.env` file.

### 2. **Prompting**
- **Zero-Shot Prompting**: Directly ask the model without examples.  
- **Dynamic Prompting**: User input is dynamically included in the prompt.  
- **Temperature / Top-P / Top-K**: Adjust creativity and randomness in responses.  

### 3. **Token Management**
- After every AI call, token usage is logged in the console.  
- This helps measure **cost efficiency** and optimize prompts.  

### 4. **Scalability**
- The system is designed to handle multiple users.  
- By caching frequent queries and limiting token usage, the bot stays efficient even under heavy traffic.  


