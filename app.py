import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System role prompt
system_prompt = """
You are an AI Career Info Agent. 
Your only job is to ask smart follow-up questions to collect ALL the important details about the user for career guidance. 
Do not give career advice yet — just ask questions.

Rules:
- Ask ONE question at a time, like a natural chat.  
- Always build on what the user just said.  
- Cover all the following areas by the end of the conversation:  
  1. Education level & study background (past + current + future plans)  
  2. Interests & favorite subjects  
  3. Skills & strengths (both technical and soft skills)  
  4. Personality traits (how they describe themselves)  
  5. Work style (alone/team, structured/flexible, remote/on-site, hands-on/creative, etc.)  
  6. Lifestyle goals (salary, freedom, balance, helping others, travel, etc.)  
  7. Inspirations & role models (and why they admire them)  
  8. Problem-solving & creativity style  
  9. Career aspirations (short-term and long-term vision)  
  10. Future skills they want to learn or improve  
- Be conversational, encouraging, and adaptive.  
- Stop after ~15 questions and say:  
  "✅ Thanks! I’ve collected enough info about you. Ready to suggest career options!"  

Now, based on this conversation so far, ask the next best follow-up question.
"""

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = [{"role": "system", "content": system_prompt}]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "started" not in st.session_state:
    st.session_state.started = False

# Streamlit UI
st.set_page_config(page_title="AI Career Info Agent", layout="centered")
st.title("🎓 AI Career Info Agent")
st.write("Answer the questions step by step, and I’ll collect info about your career interests!")

# ✅ Trigger first question automatically
if not st.session_state.started:
    first_question = "Hi! Let’s begin. What is your current education level?"
    st.session_state.conversation.append({"role": "assistant", "content": first_question})
    st.session_state.chat_history.append({"role": "assistant", "content": first_question})
    st.session_state.question_count += 1
    st.session_state.started = True

# Display conversation history
for entry in st.session_state.chat_history:
    if entry["role"] == "assistant":
        st.chat_message("assistant").write(entry["content"])
    else:
        st.chat_message("user").write(entry["content"])

# Input box
if user_input := st.chat_input("Type your answer here..."):
    # Add user message
    st.session_state.conversation.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Ask next question if limit not reached
    if st.session_state.question_count < 15:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # use gpt-3.5-turbo if quota is low
            messages=st.session_state.conversation,
            temperature=0.7
        )
        question = response.choices[0].message.content.strip()

        # Save bot response
        st.session_state.conversation.append({"role": "assistant", "content": question})
        st.session_state.chat_history.append({"role": "assistant", "content": question})
        st.session_state.question_count += 1

        # Show bot message
        st.chat_message("assistant").write(question)
    else:
        st.chat_message("assistant").write("✅ Thanks! I’ve collected enough info about you.")
