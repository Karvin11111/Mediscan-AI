# MediScan AI — Setup Guide
# ===========================
# Follow these steps exactly. Takes about 5 minutes.

# ─── STEP 1: Get your FREE Groq API Key ───
# 1. Go to: https://console.groq.com
# 2. Sign up (free)
# 3. Click "API Keys" in the left menu
# 4. Click "Create API Key"
# 5. Copy the key (starts with gsk_...)

# ─── STEP 2: Paste your key into app.py ───
# Open app.py and find this line near the top:
#
#   GROQ_API_KEY = "paste_your_groq_api_key_here"
#
# Replace the placeholder with your actual key:
#
#   GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxxxxxxx"

# ─── STEP 3: Install Python packages ───
# Open Terminal (or Command Prompt) in this folder and run:

pip install flask flask-cors groq

# ─── STEP 4: Start the backend ───
# In the same terminal, run:

python app.py

# You should see:
#   ✅ MediScan AI backend is running!
#   📡 Server: http://localhost:5000

# ─── STEP 5: Open the frontend ───
# Open the file: ai-health-assistant.html
# Just double-click it in your file explorer — it opens in your browser.

# ─── DONE! ───
# Upload a medical image and click Analyze Image.
# The frontend talks to your Python backend,
# which calls Groq AI and returns the report.

# ─── TROUBLESHOOTING ───
# • "ModuleNotFoundError" → run: pip install flask flask-cors groq
# • "Connection refused"  → make sure app.py is running (Step 4)
# • "Invalid API key"     → double-check your key in app.py
