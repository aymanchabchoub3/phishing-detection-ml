# URL & Content‑Based Phishing Website Detection

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A full end‑to‑end machine‑learning pipeline to **detect phishing websites** by combining URL analysis with page‑content inspection—and deploy the best model in a **Chrome extension** for real‑time protection.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Installation & Setup](#installation--setup)
4. [Data Collection](#data-collection)
5. [Feature Extraction](#feature-extraction)
6. [Model Training & Evaluation](#model-training--evaluation)
7. [Deployment](#deployment)
8. [Roadmap & Best Practices](#roadmap--best-practices)
9. [References](#references)

---

## 🚀 Project Overview

This repository implements a complete workflow:

1. **Data Collection**
   - Crawl and label phishing vs. legitimate URLs.
2. **Feature Extraction**
   - Derive 70+ signals from the URL, static HTML, and dynamic JavaScript.
3. **Model Training & Evaluation**
   - Compare KNN, Decision Tree, Random Forest, Gradient Boosting, CatBoost, XGBoost.
4. **Deployment**
   - Serve predictions via a Flask API.
   - Package as a Chrome extension for live browsing protection.

---

## 📁 Repository Structure

```
URL-Phishing-Detection/
├── README.md
├── LICENSE
├── requirements.txt
├── data/
│   ├── raw/
│   ├── processed/
│   └── scripts/
│       └── websites_collection.py
├── notebooks/
│   └── training.ipynb
├── src/
│   ├── features/
│   │   ├── url_features.py
│   │   ├── html_features.py
│   │   └── __init__.py
│   ├── models/
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   └── __init__.py
│   ├── inference/
│   │   └── predict.py
│   └── utils/
│       └── config.py
├── app/
│   └── flask_app.py
├── extension/
│   └── chrome/
├── assets/
│   └── mindmap.png
└── tests/
    └── test_features.py
```

---

## 🔧 Installation & Setup

1. **Clone the repo**

   ```bash
   git clone https://github.com/HarryD97/URL-Content-based-Phishing-Website-Detection-using-Machine-Learning.git
   cd URL-Content-based-Phishing-Website-Detection-using-Machine-Learning
   ```

2. **Create & activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download ChromeDriver**

   - Ensure the version matches your Chrome browser.
   - Place it on your system `PATH` or in the project root.

---

## 🌐 Data Collection

### 1. Phishing URLs

- Source: PhishTank (`verified_online.csv`)

### 2. Legitimate URLs

- Source: Tranco top sites (`tranco_list.csv`)

Run the crawler/extraction script in batches:

```bash
python data/scripts/websites_collection.py \
  --input data/raw/verified_online.csv \
  --output data/processed/phishing_websites.csv \
  --label 1 \
  --start 0 --end 10000 \
  --threads 32

python data/scripts/websites_collection.py \
  --input data/raw/tranco_list.csv \
  --output data/processed/legitimate_websites.csv \
  --label 0 \
  --start 0 --end 10000 \
  --threads 16
```

---

## 🔍 Feature Extraction

### URL‑Based Features (≈23)

- IP usage, length, shorteners, symbols (`@`, `//`), subdomains, HTTPS, redirects, domain age, custom port, traffic rank, PageRank, backlinks, etc.

### Content‑Based Features

- **Static (≈50):** HTML tag counts, text length, form inputs, headers, scripts, iframes, meta tags…
- **Dynamic:** JavaScript behaviors (pop‑ups, cookie/manipulation, hidden elements, redirections, form actions, clipboard monitoring).

> **Tip:** Inspect `src/features/url_features.py` and `src/features/html_features.py` for full details.

---

## 🤖 Model Training & Evaluation

We benchmark six classifiers:

| Model              | Key Strength                        |
| ------------------ | ----------------------------------- |
| **KNN**            | Simple, no model fitting            |
| **Decision Tree**  | Interpretability, fast inference    |
| **Random Forest**  | Robust, high accuracy, low overfit  |
| **Gradient Boost** | Sequential error correction, strong |
| **CatBoost**       | Native categorical handling         |
| **XGBoost**        | Regularized, scalable, performant   |

Workflow (see `notebooks/training.ipynb`):

1. Load features CSVs, concatenate, and split (80/20).
2. Normalize continuous features.
3. Hyperparameter tuning via cross‑validation.
4. Train final models and record:

   - **Metrics:** Accuracy, Precision, Recall, F1‑Score
   - **Timing:** Training & prediction durations

5. Visualize comparisons and select the best (e.g., Random Forest ~97% accuracy).

---

## 🚀 Deployment

### Flask API

```bash
cd app
python flask_app.py
```

- **Endpoint:** `POST /check_url`

  - **Request JSON:** `{ "url": "https://example.com" }`
  - **Response JSON:**

    ```json
    {
      "url": "https://example.com",
      "is_phishing": false,
      "confidence": 0.92
    }
    ```

### Chrome Extension

1. Navigate to `chrome://extensions`.
2. Enable **Developer mode**.
3. Click **Load unpacked** and select `extension/chrome/`.
4. Click the extension icon on any page to see the phishing verdict.

---

## 🛣️ Roadmap & Best Practices

1. **Exploratory Data Analysis (EDA)**

   - Inspect shapes, distributions, missing values.

2. **Feature Validation**

   - Test individual feature functions on known URLs.

3. **Mini‑Pipeline Prototype**

   - Extract features for a small URL set and verify DataFrame.

4. **Baseline Model**

   - Fit a shallow Decision Tree; confirm end‑to‑end flow.

5. **Scale & Automate**

   - Batch extraction, loop through models, log results.

6. **Testing & CI**

   - Add unit tests under `tests/`; integrate with GitHub Actions.

7. **Monitoring & Logging**

   - Instrument the Flask API for latency and errors.

---

## 📚 References

1. Mao et al., **“Phishing‑Alarm”**, _IEEE Access_, 2017.
2. Marchal et al., **“Off‑the‑Hook”**, _IEEE Trans. Computers_, 2017.
3. UCI Phishing Websites Dataset.
4. [Content‑Based Phishing Detection Example](https://github.com/emre-kocyigit/phishing-website-detection-content-based)

---

> _Security is a continuous journey. Keep iterating on features, models, and deployment to stay ahead._
