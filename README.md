# 🔥 Greeks + Heat

Welcome to **Greeks + Heat**, a full-stack interactive web application designed to visualize and analyze **options greeks** and **price heatmaps** for equity derivatives. Whether you're a finance enthusiast or an active trader, this project helps you better understand how strike prices and expiration dates impact the greeks of call and put options using visual heatmaps.

Built using:

- 🐍 Python (Flask) for backend  
- ⚛️ React for frontend  
- 📊 Matplotlib + NumPy for data processing and heatmap generation  
- 📦 yFinance for real-time options data  
- 🎨 Styled for a clean, responsive UI/UX  

---

## 📦 Features

- Visual heatmaps of **Delta, Gamma, Theta, Vega, Rho**
- Interactive dropdowns for **option type**, **volatility model**, **time to expiry**, and **strike price**
- API integration between frontend and backend
- Support for different volatility calculation methods (Historical, Parkinson’s, Yang-Zhang, etc.)
- Built-in error handling and loading animations

---

## 🛠️ Local Setup Guide

> 💡 **Tip:** Recommended to use macOS/Linux terminal or WSL on Windows for compatibility.

### 🚀 Step-by-Step Instructions

---

### 1. **Fork and Clone the Repo**

1. Hit the **Fork** button on GitHub to copy the repo to your account.  
2. Clone the forked repo into your machine (VSCode is preferred)

### 2. **Get the environment set up**

1. Open a new terminal and run these commands:

```zsh
python -m venv venv
source venv/bin/activate
```

This will create and run the virtual environment. Next:

```zsh
cd backend 
pip install -r requirements.txt
```

This will install all our dependencies. Now, we need to check for port collisions before we launch our backend. In the terminal run:

```zsh 
lsof -i :8000
```

If you dont see anything pop up then you are good to go onto Step 3.
If you do, run the command again with different numbered ports until nothing pops up.
With the empty port number, go to:

# app.py
# App.js 

and change all instances of 8000 to the free port number.

### 3. **Running the environment**