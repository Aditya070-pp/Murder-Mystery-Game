# 🕵️‍♂️ The Secret of Blackwood Manor - Web App

A responsive, dynamic AI-powered murder mystery game built with Python and Streamlit. Play offline or hook up your Gemini API key to dynamically construct case files and plot twists in real time!

---

## 🚀 How to Deploy on the Web (Share with Friends!)

You can host this game on the web for **free** using **Streamlit Community Cloud**.

### Step 1: Push code to GitHub
1. Create a new repository on GitHub (e.g., `murder-mystery-game`).
2. Initialize git and push the files in this directory to your repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Streamlit Murder Mystery game"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Cloud
1. Visit **[Streamlit Community Cloud](https://streamlit.io/cloud)** and click **Sign Up** (use your GitHub account).
2. Log in and click **New App** (or **Create App**).
3. Select your repository:
   - **Repository**: `YOUR_USERNAME/YOUR_REPO_NAME`
   - **Branch**: `main`
   - **Main file path**: `app.py`

### Step 3: Add your Gemini API Key (Secret Configuration)
Before clicking deploy, click **Advanced settings...** at the bottom:
1. In the **Secrets** section, type your API key in TOML format:
   ```toml
   GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
   ```
2. Click **Save**.
3. Click **Deploy!**

Your website will be live in under 2 minutes at a custom URL (e.g., `https://blackwood-manor.streamlit.app`) which you can copy and share with anyone!

---

## 💻 How to Run Locally

If you want to run the game on your own machine:

1. **Install requirements**:
   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Configure API Key (Optional)**:
   Create a `.env` file in the root directory and add your key:
   ```env
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
   ```

3. **Launch the Server**:
   ```bash
   python -m streamlit run app.py
   ```
   Open your browser to `http://localhost:8501` to play!
