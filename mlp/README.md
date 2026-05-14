# 🏥 Healthcare Fraud Detection
### UGASS Data Science Club × Zindi — ML Capstone Project

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange) ![XGBoost](https://img.shields.io/badge/XGBoost-Modeling-green) ![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📌 Project Overview

This project builds a machine learning pipeline to automatically detect fraudulent healthcare insurance claims. Using a dataset of 10,000 insurance claims, we trained and compared multiple classification models to flag suspicious claims before payout.

**The key challenge:** only 8.3% of claims are fraudulent — a highly imbalanced dataset where accuracy alone is a misleading metric. Our solution prioritises **F1-Score** and **ROC-AUC** as the true measures of success.

---

## 🏆 Results

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 98.2% | 93.1% | 87.5% | 90.2% | 99.9% |
| Random Forest | 99.5% | 96.8% | 96.0% | 96.4% | 99.9% |
| XGBoost | 99.4% | 96.2% | 96.8% | 96.5% | 99.9% |

**🥇 Winning Model: Tuned Random Forest** — F1-Score: **96.8%** | ROC-AUC: **99.9%**  
5-Fold Cross-Validation Mean F1: **96.77%** (Std: 0.006) — stable and reliable.

---

## 📁 Repository Structure

```
healthcare-fraud-detection/
│
├── data/
│   ├── healthcare_fraud_detection.csv   ← raw dataset
│   ├── X_train.csv                      ← clean training features
│   ├── X_test.csv                       ← clean test features
│   ├── y_train.csv                      ← training labels
│   └── y_test.csv                       ← test labels
│
├── notebooks/
│   ├── 01_EDA.ipynb                     ← exploratory data analysis
│   ├── 02_Data_Engineering.ipynb        ← preprocessing & feature engineering
│   ├── 03_Modeling.ipynb                ← baseline model training & evaluation
│   └── 04_Tuning.ipynb                  ← hyperparameter tuning & final model
│
├── plots/                               ← all saved charts and visualisations
│
├── README.md
└── requirements.txt
```

---

## 🔍 Dataset

- **Source:** Provided dataset (UGASS DSC × Zindi Capstone)
- **Size:** 10,000 rows × 20 columns
- **Target:** `Is_Fraud` (1 = Fraud, 0 = Not Fraud)
- **Class balance:** 91.7% Not Fraud / 8.3% Fraud

**Key features:**
- `Claim_Amount` — total amount claimed
- `Approved_Amount` — amount approved by insurer
- `Days_Between_Service_and_Claim` — delay from service to filing
- `Provider_ID` — the healthcare provider
- `Insurance_Type`, `Visit_Type`, `Provider_Specialty`

---

## ⚙️ Methodology

### 1. Exploratory Data Analysis
- Identified class imbalance (8.3% fraud)
- Found fraudulent claims average ~$990 vs ~$535 for legitimate claims
- Discovered fraud clusters around specific providers
- Identified 350 missing values in 3 columns

### 2. Data Preprocessing
- Dropped `Claim_ID` and `Claim_Submission_Date` (no predictive value)
- Filled missing categoricals with **mode**, numericals with **median**
- One-Hot Encoded all categorical variables (41 final features)
- Train/test split: **80/20** with `stratify=y` to preserve fraud ratio
- Applied `StandardScaler` fitted on training data only (no data leakage)

### 3. Feature Engineering (3 new features)
| Feature | Formula | Why It Matters |
|---|---|---|
| `claim_to_approved_ratio` | Claim_Amount / (Approved_Amount + 1) | Fraudsters over-claim vs approved — ratio is ~2× higher |
| `provider_fraud_rate` | Historical fraud % per provider | Fraud clusters around specific providers |
| `claim_per_day` | Claim_Amount / (Length_of_Stay + 1) | Inflated daily cost signals fraud |

### 4. Modeling
All models were configured to handle class imbalance:
- **Logistic Regression** — `class_weight='balanced'`
- **Random Forest** — `class_weight='balanced'`
- **XGBoost** — `scale_pos_weight=11.07` (imbalance ratio)

### 5. Hyperparameter Tuning
Used `RandomizedSearchCV` with 20 iterations × 5-fold cross-validation on the best model (Random Forest).

**Best parameters found:**
```
n_estimators:      300
max_depth:         None
min_samples_split: 5
min_samples_leaf:  4
max_features:      log2
class_weight:      balanced
```

---

## 📊 Top Features Driving Predictions

1. `claim_to_approved_ratio` — **44.7%** importance *(engineered feature)*
2. `Days_Between_Service_and_Claim` — **27.4%** importance
3. `Claim_Amount` — **6.4%** importance
4. `Claim_Status_Rejected` — **4.1%** importance
5. `provider_fraud_rate` — **3.9%** importance *(engineered feature)*

> Two of the top 5 features were ones **we created** — validating the value of feature engineering.

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.x
- pip

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the notebooks in order
```bash
jupyter notebook
```
Open and run each notebook in `/notebooks/` sequentially:
1. `01_EDA.ipynb`
2. `02_Data_Engineering.ipynb`
3. `03_Modeling.ipynb`
4. `04_Tuning.ipynb`

> **Note:** Update the file paths at the top of each notebook to match your local machine.

---

## 📦 Requirements

See `requirements.txt`:
```
pandas
numpy
matplotlib
seaborn
scikit-learn
xgboost
jupyter
```

---

## 💡 Key Takeaways

- **Accuracy is not enough** for imbalanced datasets — always check F1 and ROC-AUC
- **Feature engineering** was critical: `claim_to_approved_ratio` alone explains 44.7% of model decisions
- **Data leakage** must be avoided — scale and encode after splitting, not before
- **Provider history** is a powerful signal — fraud clusters around specific providers
