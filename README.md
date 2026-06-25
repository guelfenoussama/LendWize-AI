# # Lendwise AI • Smart Loan Risk & DSCR Prediction System

**Smart Loan Intelligence • Optimized for the Indian Banking Ecosystem using Real-World Financial Data**

This repository contains an end-to-end Machine Learning system. The architecture processes customer financial profiles to predict loan default probabilities and calculate the Debt Service Coverage Ratio (DSCR). The project covers the full development cycle: from data preprocessing and model selection to containerization and cloud deployment.

---

## Live Production Site
The application is deployed and accessible in full-screen standalone mode here:
[Lendwise AI Web App](https://oussama-group-lendwise-ai.hf.space)

---

## Interactive Test Cases
To evaluate how the backend models and dashboard logic respond to different financial profiles, you can input these test cases on the live site:

* **Case A (Low-Risk Profile):** Input a high annual income relative to a low requested loan amount, backed by stable asset values. The system will compute a high DSCR and trigger a **"Healthy"** risk status (displayed in green).
* **Case B (High-Risk Profile):** Input a low annual income with a maximum loan amount. The Flask backend will identify the risk threshold breach, flag the status as **"Declined"** with the calculated statistical confidence score, and trigger the internal system risk notification.

---

## Technical Domain & Constraints (Indian Banking Sector)
* **INR Currency Only:** The models were trained strictly on financial data from the Indian banking ecosystem.
* **Operational Limits:** Features like annual income, asset valuation, and loan parameters are mapped to Indian Rupees (INR). Converting these inputs into USD breaks the underlying statistical boundaries and risk thresholds calculated during training.

---

## Engineering Challenges & Solutions

Building and deploying this system required resolving several technical problems across the data and infrastructure layers.

### 1. Model Configuration and Tuning
During the initial training phase, the baseline models returned an AUC = 0.9.

* **The Discovery:** While double-checking the features, I verified that this was not caused by data leakage. Instead, it was the result of natural **Bias Mitigation** within the dataset configuration.
* **The Result:** To make sure the system works perfectly, I compared 4 machine learning models for classification and 4 machine learning models for regression, then selected the best performing ones for the final system.

### 2. Cloud Deployment
I uploaded the application to a live cloud server so anyone can use it online.

* **Server Setup:** I configured all the Python environment libraries to make the app run online.
* **Custom CSS:** I used custom HTML and CSS to fix the UI design, remove the host borders, and change the look to match my group's branding.
* **API Connection:** I connected the Streamlit UI directly to the Flask backend to allow data exchange via JSON payloads.

### 3. Final Integration
By connecting the backend and the hosting platform, the system achieved full stability. The entire architecture now runs smoothly under a dedicated space (`oussama-group`).

---

## System Architecture

The project uses two main parts that talk to each other using structured JSON payloads:
* **Backend API (Flask Engine):** Deployed on port `9697`. It receives the customer data, sends it through the machine learning models, and outputs the final risk metrics.
* **Frontend Dashboard (Streamlit UI):** Deployed on port `8501`. I used custom HTML5 and CSS3 to fix the cloud platform design and control the dashboard layout.

---

## Core Technical Features

* **UI Theme Toggle:** Custom CSS code automatically changes the dashboard colors and fonts to match the user's light or dark system theme.
* **Data Validation:** The system safely accepts different financial inputs and handles errors if the values are unexpected.
* **Direct Network Access:** The deployment is configured for fast global access without proxy delays or loading issues.

---

## Developer

* **Oussama** (17 years old, Algeria 🇩🇿)
* **Education:** Built using self-learning through the **Machine Learning Zoomcamp** course.

This project demonstrates skills in full-stack data engineering and machine learning: from analyzing data to deploying a live web application.
