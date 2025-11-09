import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Set page config
st.set_page_config(
    page_title="Data Scientist Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Tailwind CSS via CDN
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<style>
/* Custom overrides jika perlu, tapi Tailwind handle sebagian besar */
.stApp {
    background: linear-gradient(135deg, #dbeafe, #fce7f3); /* Tailwind blue-100 to pink-100 */
}
</style>
""", unsafe_allow_html=True)

# Fungsi generate respons (tetap sama)
def generate_response(prompt, history):
    context = "\n".join(history[-5:])
    full_prompt = (
        f"Kamu adalah asisten produktivitas data scientist yang santai dan membantu. "
        f"Gunakan gaya bahasa ramah, seperti 'bro' atau emoji. "
        f"Fokus pada data science, ML, Python, dan statistik.\n\n"
        f"Konteks sebelumnya:\n{context}\n\n"
        f"Pengguna: {prompt}"
    )
    try:
        response = model.generate_content(full_prompt)
        return response.text or "😅 Maaf bro, aku belum dapat jawabannya."
    except Exception as e:
        return f"⚠️ Terjadi error: {e}"

# Fungsi rekomendasi dataset (tetap sama)
def recommend_dataset(query):
    if "machine learning" in query.lower() or "ml" in query.lower():
        return "Coba dataset Iris: https://www.kaggle.com/uciml/iris"
    elif "regression" in query.lower():
        return "Dataset Boston Housing: https://www.kaggle.com/vikrishnan/boston-house-prices"
    else:
        return "Dataset Titanic untuk analisis: https://www.kaggle.com/c/titanic"

# UI dengan Tailwind classes
st.markdown('<h1 class="text-4xl font-bold text-center text-teal-600 mb-6">🤖 Data Scientist Productivity Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="text-lg text-center text-gray-700 mb-8">Halo bro! Saya asisten AI untuk bantu kamu dengan data science. Tanya tentang ML, Python, atau rekomendasi dataset! 😎</p>', unsafe_allow_html=True)

# Sidebar untuk history
with st.sidebar:
    st.markdown('<h2 class="text-xl font-semibold text-gray-800 mb-4">📜 Riwayat Percakapan</h2>', unsafe_allow_html=True)
    if "history" not in st.session_state:
        st.session_state.history = []
    for msg in st.session_state.history[-10:]:
        st.markdown(f'<div class="bg-white bg-opacity-80 rounded-lg p-4 mb-2 shadow-md">{msg}</div>', unsafe_allow_html=True)

# Main area
col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.text_input("Apa yang bisa saya bantu hari ini?", key="input", help="Tanya apa saja tentang data science!")
    if st.button("Kirim", key="send", help="Kirim pesan"):
        response = generate_response(user_input, st.session_state.history)
        if "dataset" in user_input.lower() or "data" in user_input.lower():
            response += f"\n\nRekomendasi dataset: {recommend_dataset(user_input)}"
        st.session_state.history.append(f"Pengguna: {user_input}")
        st.session_state.history.append(f"Asisten: {response}")
        st.markdown(f'<div class="bg-white bg-opacity-80 rounded-lg p-4 shadow-md mt-4">**Asisten:** {response}</div>', unsafe_allow_html=True)