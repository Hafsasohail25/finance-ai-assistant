import os
import requests
import pandas as pd
from dotenv import load_dotenv
from extractor import extract_text_from_pdf
from classifier import parse_transactions

load_dotenv()

def chat_with_together(user_input):
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        return "❌ Together.ai API key not found."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "You are a helpful finance assistant."},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 500,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ Together.ai error: {str(e)}"

def process_uploaded_pdf(uploaded_file):
    try:
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        filepath = os.path.join(temp_dir, uploaded_file.name)

        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        extracted_text = extract_text_from_pdf(filepath)
        transactions = parse_transactions(extracted_text)

        # Create DataFrame
        df = pd.DataFrame(transactions)

        # ✅ Fix: Parsing dates with dayfirst=True to handle DD/MM/YYYY format
        df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors='coerce')
        df = df.dropna(subset=["date"])  # Drop rows with invalid dates

        os.remove(filepath)

        # ✅ Return the DataFrame and no error
        return df, None

    except Exception as e:
        # ✅ Return an empty DataFrame and the error message
        return pd.DataFrame(), f"⚠ Error processing PDF: {str(e)}"

