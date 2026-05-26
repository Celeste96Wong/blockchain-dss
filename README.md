# BlockchainReady — AI-Powered Fuzzy MCDM DSS

> **FYP Prototype** · Fuzzy AHP + TOPSIS + GPT-4o-mini  
> Research Topic: *A Fuzzy MCDM Decision Tool for Blockchain Adoption Readiness in SMEs*

---

## What This Does

BlockchainReady is a web-based Decision Support System (DSS) that helps non-technical SME owners assess whether their business is ready to adopt Blockchain technology.

**Under the hood:**
- **Fuzzy AHP** — Pre-calibrated expert weights for 7 adoption criteria (TOE framework)
- **Fuzzy TOPSIS** — Computes a Closeness Coefficient (CC) as the readiness score
- **GPT-4o-mini** — Translates mathematical output into plain-language recommendations
- **Flask** — Lightweight Python web framework
- **Vercel** — Free cloud deployment

---

## Project Structure

```
blockchain-dss/
├── app.py                  ← Flask entry point
├── requirements.txt        ← Python dependencies
├── vercel.json             ← Vercel deployment config
├── core/
│   ├── __init__.py
│   ├── fuzzy_engine.py     ← Fuzzy AHP + TOPSIS logic
│   └── ai_advisor.py       ← OpenAI recommendation generator
└── templates/
    └── index.html          ← Full frontend UI
```

---

## Setup (Local — VS Code)

### Step 1 — Clone or download the project

If using GitHub:
```bash
git clone https://github.com/YOUR_USERNAME/blockchain-dss.git
cd blockchain-dss
```

Or just open the folder in VS Code directly.

### Step 2 — Create a virtual environment

Open VS Code terminal (`Ctrl + `` ` ``) and run:

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

This installs Flask, OpenAI, NumPy, and scikit-fuzzy. Takes about 1–2 minutes.

### Step 4 — Run the app

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

Open your browser and go to: **http://localhost:5000**

---

## How to Use the App

1. **Step 1 — Business Context**
   - Select your industry, company size, and main goal
   - Enter your OpenAI API key (starts with `sk-...`)
   - The API key is sent directly to OpenAI and never stored

2. **Step 2 — Assessment**
   - Rate 7 criteria using sliders (1 = Very Low, 5 = Very High)
   - Be honest — there are no right or wrong answers
   - Click "Analyse My Readiness"

3. **Step 3 — Results**
   - See your Readiness Score (0–100) with Fuzzy TOPSIS Closeness Coefficient
   - View per-criterion breakdown
   - Read your AI-generated personalised recommendation

---

## Deploy to Vercel (Free)

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: BlockchainReady prototype"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/blockchain-dss.git
git push -u origin main
```

### Step 2 — Deploy on Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click **"New Project"**
3. Import your `blockchain-dss` repository
4. Vercel auto-detects the `vercel.json` config
5. Click **"Deploy"**
6. Your app will be live at `https://blockchain-dss-YOUR_USERNAME.vercel.app`

> ✅ Vercel free tier is sufficient for this prototype

---

## The 7 Assessment Criteria (TOE Framework)

| # | Criterion | Framework Layer | Fuzzy Weight |
|---|-----------|----------------|--------------|
| 1 | Data Integrity Need | Technology | High (5,7,9) |
| 2 | Multi-Party Trust Issues | Technology | High (5,7,9) |
| 3 | Transparency Requirement | Organisation | Medium (3,5,7) |
| 4 | Process Automation Potential | Technology | Medium (3,5,7) |
| 5 | Technical Readiness | Organisation | Low (1,3,5) |
| 6 | Budget Availability | Organisation | Low (1,3,5) |
| 7 | Regulatory Compliance Pressure | Environment | Medium (3,5,7) |

---

## Fuzzy TOPSIS — How It Works

```
User Answer (1–5)
      ↓
Triangular Fuzzy Number (TFN)
e.g. rating 4 → (5, 7, 9)
      ↓
Weighted Fuzzy Decision Matrix
(TFN × normalised Fuzzy AHP weight)
      ↓
Distance from Fuzzy Positive Ideal Solution (FPIS)  →  D+
Distance from Fuzzy Negative Ideal Solution (FNIS)  →  D-
      ↓
Closeness Coefficient CC = D- / (D+ + D-)
      ↓
Readiness Score = CC × 100
```

**Tier Classification:**
- 🟢 **High Readiness** — CC ≥ 0.70 (Score ≥ 70)
- 🟡 **Moderate Readiness** — CC 0.45–0.69 (Score 45–69)
- 🔴 **Low Readiness** — CC < 0.45 (Score < 45)

---

## Research Context

This prototype demonstrates the feasibility of:
- Simplifying expert-level Fuzzy MCDM for non-technical end users
- Combining quantitative (Fuzzy TOPSIS) with generative AI (LLM) for explainable DSS
- Applying the TOE framework to Blockchain adoption assessment in SMEs

**Key references:**
- Chang, D.Y. (1996) — Fuzzy AHP method
- Hwang & Yoon (1981) — Original TOPSIS
- Rogers (2003) — TOE Framework for technology adoption
- TAM (Davis, 1989) — Technology Acceptance Model

---

## Extending This Prototype

For the full FYP implementation, consider adding:

- [ ] User authentication + saved assessments (SQLite)
- [ ] Comparison view — compare multiple business profiles
- [ ] Sensitivity analysis — show how changing one criterion affects the score
- [ ] Admin panel — for researchers to view aggregate data
- [ ] Multi-language support (BM + English for Malaysian SMEs)
- [ ] Export to PDF report
- [ ] Validated Fuzzy AHP weights from expert survey (Delphi method)

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | Python + Flask | Lightweight, easy to deploy |
| Fuzzy Math | NumPy + scikit-fuzzy | Standard scientific Python |
| AI Layer | OpenAI GPT-4o-mini | Cost-effective, strong reasoning |
| Frontend | Vanilla HTML/CSS/JS | No build step, instant deploy |
| Deployment | Vercel | Free, GitHub-integrated |

---

*Prototype built for FYP Research Demonstration · Not for commercial use*


# 1. 創建虛擬環境
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 2. 安裝依賴
pip install -r requirements.txt
pip install flask openai numpy scikit-fuzzy networkx gunicorn

# 3. 運行
python app.py

# 4. 退出 venv
deactivate
