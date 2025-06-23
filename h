import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV,
    cross_val_score,
    KFold
)
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from scipy.stats import randint

# ========== STEP 1: Load and Prepare Data ==========

# Load your final cleaned dataset (no missing 'Total_Rainfall')
final_df = pd.read_csv("final_corrected_dataset_final_filled_v2.csv")

# (Optional) Handle outliers or transform yield, if desired:
# q1 = final_df["Yield"].quantile(0.25)
# q3 = final_df["Yield"].quantile(0.75)
# iqr = q3 - q1
# lower_bound = q1 - 1.5 * iqr
# upper_bound = q3 + 1.5 * iqr
# final_df = final_df[final_df["Yield"].between(lower_bound, upper_bound)]
# OR
# final_df["Yield"] = np.log1p(final_df["Yield"])  # log-transform

# Define features (X) and target (y)
feature_cols = ["Total_Rainfall", "Area"] + [col for col in final_df.columns if col.startswith("Crop_")]
target_col = "Yield"

X = final_df[feature_cols]
y = final_df[target_col]

# ========== STEP 2: Train-Test Split ==========
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Data split complete. Training size:", X_train.shape, "Test size:", X_test.shape)

# ========== STEP 3: Hyperparameter Tuning with Randomized Search + Cross-Validation ==========

# Define the parameter distribution for Random Forest
param_dist = {
    "n_estimators": randint(50, 200),
    "max_depth": randint(3, 20),
    "min_samples_split": randint(2, 10),
    "min_samples_leaf": randint(1, 10)
}

# Set up RandomizedSearchCV
rf_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=1)

random_search = RandomizedSearchCV(
    rf_model,
    param_distributions=param_dist,
    n_iter=10,               # Number of random configurations to try
    scoring="neg_mean_squared_error",  # Could also use "r2"
    cv=3,                    # 3-fold cross-validation
    verbose=1,               # Print progress
    random_state=42,
    n_jobs=-1                # Use all available CPU cores
)

print("\nStarting Randomized Search...\n")
random_search.fit(X_train, y_train)

print("Best parameters found:", random_search.best_params_)
print("Best score (CV RMSE):", np.sqrt(-random_search.best_score_))

# Retrieve the best model
best_model = random_search.best_estimator_

# ========== STEP 4: Evaluate with Cross-Validation (Optional Extra Check) ==========

kfold = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(
    best_model, X_train, y_train, cv=kfold, scoring="r2", n_jobs=-1
)

print("\nCross-Validation R² Scores:", cv_scores)
print("Mean CV R²:", cv_scores.mean(), "Std Dev CV R²:", cv_scores.std())

# ========== STEP 5: Final Training on the Entire Training Set and Test Evaluation ==========

best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)

r2 = r2_score(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)

print("\nFinal Model Performance on Test Set:")
print(f"R² Score: {r2:.4f}")
print(f"RMSE: {rmse:.4f}")

# Compare Train vs. Test to check for overfitting
y_train_pred = best_model.predict(X_train)
train_r2 = r2_score(y_train, y_train_pred)
train_rmse = mean_squared_error(y_train, y_train_pred, squared=False)
print(f"Train R²: {train_r2:.4f}, Train RMSE: {train_rmse:.4f}")

# ========== STEP 6: Feature Importance ==========

importances = best_model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
plt.title("Feature Importances (Optimized RF)")
plt.bar(range(len(feature_cols)), importances[indices], color="royalblue", align="center")
plt.xticks(range(len(feature_cols)), [feature_cols[i] for i in indices], rotation=45, ha="right")
plt.ylabel("Importance")
plt.tight_layout()
plt.show()

# ========== STEP 7: Correlation Matrix ==========

plt.figure(figsize=(8, 6))
corr_matrix = final_df[["Yield", "Production", "Total_Rainfall", "Area"]].corr()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix (Key Variables)")
plt.tight_layout()
plt.show()




print("\nAll steps completed successfully!")
