import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
# Tambah konfigurasi untuk force versi API atau client options
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Coba v1beta atau v1
model = genai.GenerativeModel("models/gemini-2.5-flash")  # Pakai model yang kamu mau

try:
    response = model.generate_content("Halo, test saja")
    print("Respons:", response.text)
except Exception as e:
    print("Error:", e)