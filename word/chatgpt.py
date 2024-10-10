"""Chat GPT LLM Clone"""

import streamlit as st
import random
import time


# Emulador de resposta
def response_generator() -> any:
    """docstring"""
    response = random.choice(
        [
            "Olá! Como eu posso te ajudar hoje?",
            "Oi, humano! Tem algo na qual eu possa te ajudar hoje?",
            "Você precisa de ajuda?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Conversa Simples")

# Inicializar o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra as mensagens do chat do histórico no reinício do aplicativo
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Aceita a entrada do usuário
if prompt := st.chat_input("Como posso ajudar?"):
   # Adiciona a resposta do usuário ao histórico do chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Mostra a mensagem do usuário em um container de mensagem no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Mostra a mensagem do assistente em um container de mensagem no chat
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Adiciona a resposta do assistente ao histórico do chat
    st.session_state.messages.append({"role": "assistant", "content": response})
