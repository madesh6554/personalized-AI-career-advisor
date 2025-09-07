import os
import openai
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = """
You are a Career Info Agent. 
Your only job is to ask structured follow-up questions to collect information about a user’s background, interests, and skills.

Rules:
1. Start by asking about education level.
2. Ask no more than 1 question at a time (chat-style).
3. Make questions short, simple, and friendly (not like a survey).
4. Cover these areas in 15–20 questions max:
   - Education Level
   - Favorite Subjects / Interests
   - Skills & Strengths
   - Personality Traits
   - Career Aspirations / Lifestyle Preferences
   - Work Environment Preference
5. DO NOT recommend careers. Just collect information.
6. Stop when you feel you have enough info (15–20 questions).
7. Output format: only the next question text (no explanation).
"""

def get_followup_question(conversation_history):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",   # or "gpt-4" if available
        messages=conversation_history,
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"].strip()

if __name__ == "__main__":
    conversation = [{"role": "system", "content": system_prompt}]
    print("Career Info Agent: Hi! Let’s begin. What is your current education level?")
    conversation.append({"role": "assistant", "content": "What is your current education level?"})
    
    for _ in range(15):
        user_input = input("You: ")
        conversation.append({"role": "user", "content": user_input})
        
        followup_q = get_followup_question(conversation)
        print(f"Career Info Agent: {followup_q}")
        conversation.append({"role": "assistant", "content": followup_q})
