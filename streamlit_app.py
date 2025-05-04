import streamlit as st
from app import process_uploaded_pdf, chat_with_together
from visualization import plot_spending_chart, plot_monthly_trend
import pandas as pd
from datetime import datetime

def auto_categorize(description):
    desc = description.lower()
    if any(x in desc for x in ["grocery", "mart", "supermarket", "store"]):
        return "Groceries"
    elif any(x in desc for x in ["uber", "transport", "bus", "taxi", "cab", "ride"]):
        return "Transport"
    elif any(x in desc for x in ["restaurant", "food", "dine", "meal", "cafe", "coffee"]):
        return "Food"
    elif any(x in desc for x in ["rent", "lease", "housing", "apartment"]):
        return "Rent"
    elif any(x in desc for x in ["salary", "income", "deposit", "paycheck"]):
        return "Income"
    elif any(x in desc for x in ["netflix", "spotify", "subscription", "entertainment"]):
        return "Entertainment"
    else:
        return "Other"

def main():
    st.set_page_config(page_title="💸 Finance AI Assistant", page_icon="💬", layout="wide")

    # 🌟 Global Style
    st.markdown("""
    <style>
        html, body {
            background-color: #121212;
            color: #F3F4F6;
            font-family: 'Segoe UI', sans-serif;
        }
        .main-container {
            max-width: 1200px;
            margin: auto;
            padding: 2rem 3rem;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 18px;
            padding: 2rem 2.5rem;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            margin-bottom: 2.5rem;
        }
        .stButton > button {
            background-color: #6366F1;
            color: white;
            padding: 0.7rem 1.5rem;
            border-radius: 10px;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #4338CA;
            transform: scale(1.02);
        }
        .hero-title {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(to right, #3B82F6, #9333EA);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0.2rem;
        }
        .hero-sub {
            text-align: center;
            font-size: 1.1rem;
            color: #9CA3AF;
            margin-bottom: 2rem;
        }
        .footer {
            margin-top: 4rem;
            text-align: center;
            font-size: 0.9rem;
            color: #6B7280;
        }
    </style>
    """, unsafe_allow_html=True)

    # 💫 Hero Section
    st.markdown("""
        <div class="glass-card">
            <div class="hero-title">Finance AI Assistant 💸</div>
            <p class="hero-sub">Smarter money decisions with AI-powered financial insights.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
<style>
body {
    background-image: url("https://cdn.pixabay.com/photo/2018/01/23/12/41/cryptocurrency-3091789_1280.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

section.main > div {
    background-color: rgba(0, 0, 0, 0.6);  /* glassmorphism dark overlay */
    padding: 2rem;
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

    # 📁 Upload Section
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📄 Upload Your Bank Statement (PDF)")
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

        if uploaded_file and uploaded_file.name.endswith('.pdf'):
            df, error = process_uploaded_pdf(uploaded_file)

            if error:
                st.error(error)
            elif not df.empty:
                st.success("✅ PDF Processed Successfully!")

                if "category" not in df.columns and "description" in df.columns:
                    df["category"] = df["description"].apply(auto_categorize)

                if "date" in df.columns:
                    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors='coerce')
                    date_range = st.date_input("📅 Filter by Date", [df["date"].min(), df["date"].max()])
                    if len(date_range) == 2:
                        df = df[(df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))]

                with st.expander("📂 View Transactions"):
                    st.dataframe(df, use_container_width=True)

                if "category" in df.columns:
                    st.subheader("📊 Summary")
                    col1, col2, col3 = st.columns(3)
                    total_spent = df["amount"].sum()
                    top_cat = df.groupby("category")["amount"].sum().idxmax()
                    top_val = df.groupby("category")["amount"].sum().max()

                    col1.metric("Total Spent", f"${total_spent:,.2f}")
                    col2.metric("Top Category", top_cat)
                    col3.metric("Spent in Top Category", f"${top_val:,.2f}")

                    chart_type = st.radio("📈 Choose chart type:", ["Bar Chart", "Monthly Trend"], horizontal=True)
                    fig = plot_spending_chart(df) if chart_type == "Bar Chart" else plot_monthly_trend(df)
                    st.pyplot(fig)

                    st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name="transactions.csv")
                    st.subheader("🧠 Get AI Financial Advice")

                    if st.button("Generate Advice"):
                        with st.spinner("Generating insights..."):
                            summary = df.groupby("category")["amount"].sum().to_string()
                            advice = chat_with_together(f"Give me budget advice for:\n\n{summary}")
                        st.info(advice)
                        st.download_button("💾 Save Advice", data=advice, file_name="financial_advice.txt")

                else:
                    st.warning("❗ Categories not found. Please ensure your file contains labeled transactions.")
            else:
                st.warning("🚫 Could not read data from PDF.")
        elif uploaded_file:
            st.warning("Please upload a valid PDF.")
        st.markdown('</div>', unsafe_allow_html=True)

    # 🤖 Chat Section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💬 Ask FinanceBot")

    query = st.text_input("💡 Type your question:")
    if st.button("📩 Ask Now"):
        if query.strip():
            with st.spinner("Thinking..."):
                reply = chat_with_together(query)
            st.success("Here’s what I found:")
            st.markdown(f"> {reply}")
        else:
            st.warning("Please type your question first.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 👣 Footer
    st.markdown("""<div class="footer">Made by Hafsa Sohail | 2025</div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
