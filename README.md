# 🕉️ Divine Hindu AI Support Bot

A WhatsApp-style AI customer support assistant built with Streamlit + Groq (LLaMA 3.1).

## ✨ Features
- WhatsApp-inspired dark UI with chat bubbles
- One-tap suggestion chips
- Order tracking for 15 demo orders (DH101–DH115)
- Powered by Groq's ultra-fast LLaMA 3.1 inference
- Fully mobile-responsive

---

## 🚀 Deploy on Streamlit Community Cloud (Recommended — Free)

> ⚠️ **Note:** This app uses Streamlit and **cannot be deployed on Vercel** (Vercel doesn't support WebSocket-based Python servers). Use **Streamlit Community Cloud** instead — it's free and purpose-built for this.

### Step 1 — Push to GitHub
```bash
git add .
git commit -m "ready to deploy"
git push origin main
```

### Step 2 — Deploy on Streamlit Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub
2. Click **"New app"**
3. Select your repository and set:
   - **Main file path:** `app_ui.py`
   - **Branch:** `main`
4. Click **"Advanced settings"** → **"Secrets"** and paste:
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   ```
5. Click **"Deploy!"** — your app will be live in ~60 seconds 🎉

---

## 💻 Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/ai-support-bot.git
cd ai-support-bot

# Install dependencies
pip install -r requirements.txt

# Add your API key
echo 'GROQ_API_KEY="your-groq-api-key"' > .env

# Run the app
streamlit run app_ui.py
```

---

## 🔑 Getting a Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Navigate to **API Keys** → **Create API Key**
4. Copy and use it in your secrets

---

## 📁 Project Structure

```
ai-support-bot/
├── app_ui.py              # Main Streamlit app (UI + AI logic)
├── requirements.txt       # Python dependencies
├── .streamlit/
│   ├── config.toml        # Server & theme config
│   └── secrets.toml       # Local secrets (git-ignored)
├── .env                   # Local env vars (git-ignored)
├── .gitignore
└── README.md
```

---

## 🛡️ Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com |

On **Streamlit Cloud**: add via the Secrets dashboard  
Locally: add to `.env` file or `.streamlit/secrets.toml`
