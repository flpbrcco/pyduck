"""Chatbot usando Streamlit e NLTK"""

# Imports
import streamlit as st
from nltk.chat.util import Chat, reflections
import json


# Carregar dataset público (pairs.json)
def load_pairs(file_path):
    '''Carrega pares de padrões e respostas de um arquivo JSON.'''
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    pairs = []
    for item in data:
        # Flatten patterns para strings regex única: "oi|olá|bom dia"
        pattern_str = '|'.join(item['patterns'])
        # responses devem ser lidas de strings
        responses = item['responses']
        pairs.append((pattern_str, responses))
        pairs.append((r'(.*)', ["Desculpe, não entendi. Pode reformular?"]))
    return pairs


pairs = load_pairs("./json/pairs.json")
chatbot = Chat(pairs, reflections)

st.title("Chatbot simples com NLTK")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = chatbot.respond(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
