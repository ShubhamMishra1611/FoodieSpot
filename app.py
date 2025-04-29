
import streamlit as st
from agent_logic import process_user_message 

st.title(" FodieSpot Reservation Assistant")
st.caption("Powered by Llama-3.1-8B (Simulated) - Built from scratch")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "history_string" not in st.session_state:
     st.session_state.history_string = "Assistant: Hello! How can I help you with your FoodieSpot reservation today?"
     
     st.session_state.messages.append({"role": "assistant", "content": st.session_state.history_string.split("Assistant: ")[1]})



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask about restaurants or reservations..."):
    
    st.chat_message("user").markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    
    
    assistant_response, updated_history = process_user_message(prompt, st.session_state.history_string)

    
    st.session_state.history_string = updated_history

    
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})