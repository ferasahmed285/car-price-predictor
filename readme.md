# Car Price Prediction Using Machine Learning

**University:** Ain Shams University - Faculty of Engineering (ICHEP)  
**Course Year:** 2025  
**Supervisor:** Eng. Heba Gamal Saleh

## 📌 Executive Summary
This project implements a machine learning system designed to predict used car market prices. By analyzing objective vehicle attributes—such as mileage, model year, and engine volume—the model addresses the challenge of subjective vehicle valuation in the pre-owned automotive market.

The system compares **Linear Regression** (Baseline) against **Ridge Regression** (L2 Regularization), demonstrating that regularization significantly improves prediction accuracy by mitigating multicollinearity.

---

## 👥 Authors
* **Ferass Ahmed Mostafa** (23P0304)
* **Hisham Mohamed Abdrabelrasoul** (23P0259)
* **Ahmed Mohamed Elmlahe** (23P0035)
* **Mohamed Bassam** (17T0338)

---

## 📂 Dataset Description
The model is trained on a structured dataset of used car listings, split into training and testing sets to evaluate performance objectively.

* **Target Variable:** Price (Continuous)
* **Key Features:**
    * **Categorical:** Manufacturer, Model, Fuel Type, Gearbox Type, Drive Wheels, Color.
    * **Numerical:** Production Year, Engine Volume, Mileage (Odometer), Cylinders, Airbags.

---

## 🛠️ Methodology & Pipeline

### 1. Data Preprocessing & Engineering
To ensure data quality, the following pipeline was applied:
* **Cleaning:** Removal of duplicate records and irrelevant features.
* **Imputation:** Statistical imputation for missing values in critical columns.
* **Outlier Removal:** Detection and removal of extreme outliers in Price and Mileage to prevent skewing.
* **Feature Encoding:** One-Hot Encoding applied to categorical variables (e.g., Fuel Type, Gearbox) to convert text labels into numerical vectors.

### 2. Exploratory Data Analysis (EDA)
Key insights derived from the data:
* **Correlation:** Strong positive correlation between Price, Production Year, and Engine Volume. Strong negative correlation with Mileage.
* **Categorical Trends:** Automatic vehicles generally command higher market values than manual ones.
* **Interaction:** Luxury manufacturers maintain higher residual values even with higher mileage.

### 3. Modeling
Two supervised regression algorithms were implemented using Python's `scikit-learn`:
1.  **Linear Regression (Baseline):** A standard Ordinary Least Squares (OLS) model.
2.  **Ridge Regression (L2 Regularization):** Adds a penalty term proportional to the square of the coefficient magnitudes to shrink less important features and reduce variance.

### 4. Hyperparameter Tuning
* **Method:** Grid Search.
* **Parameter:** Alpha (Regularization strength).
* **Outcome:** Selected an optimal alpha that minimized validation error, balancing overfitting and underfitting.

---

## 📊 Model Evaluation & Results

The models were evaluated using Mean Absolute Error (MAE), Mean Squared Error (MSE), and $R^2$ Score.

| Metric | Description | Performance (Ridge vs. Linear) |
| :--- | :--- | :--- |
| **MAE** | Mean Absolute Error | **Lower in Ridge** (Better) |
| **MSE** | Mean Squared Error | **Lower in Ridge** (Better) |
| **$R^2$ Score** | Variance Explained | **Higher in Ridge** (Better Fit) |

**Conclusion:** Ridge Regression successfully mitigated the overfitting observed in the baseline Linear Regression model, providing a more reliable framework for automated price estimation.

---

## 🚀 Future Work
* Implementation of Ensemble Methods (Random Forest, XGBoost).
* Deployment of the model via a Flask API.
* Advanced feature engineering to capture more complex relationships.

---
## 🔧 Technologies Used
* **Language:** Python
* **Libraries:** `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `seaborn`
