import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import streamlit as st
import matplotlib.pyplot as plt
import pickle


def train_model(data):
    """Train and display a Random Forest Regressor model with hyperparameter tuning."""

    st.header("Random Forest Model Training")

    # Step 1: Allow user to select feature and target columns
    feature_columns = st.multiselect("Select Feature Columns", options=data.columns, key="rf_feature_columns")
    target_column = st.selectbox("Select Target Column", options=data.columns, key="rf_target_column")

    if not feature_columns or not target_column:
        st.warning("Please select at least one feature column and a target column.")
        return

    # Validate target column is numeric
    if not pd.api.types.is_numeric_dtype(data[target_column]):
        st.error("The target column must be numeric for regression.")
        return

    # Step 2: Split data into training and testing sets
    X = data[feature_columns]
    y = data[target_column]

    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    except ValueError as e:
        st.error(f"Error splitting data: {e}")
        return

    # Step 3: Define the Random Forest model and hyperparameter grid
    st.sidebar.header("Hyperparameter Tuning")
    n_estimators = st.sidebar.multiselect(
        "Number of Trees (n_estimators)", options=[10, 50, 100, 200, 500], default=[100], key="rf_n_estimators"
    )
    max_depth = st.sidebar.multiselect(
        "Max Depth", options=[None, 5, 10, 20, 50], default=[10], key="rf_max_depth"
    )
    min_samples_split = st.sidebar.multiselect(
        "Minimum Samples Split", options=[2, 5, 10], default=[2], key="rf_min_samples_split"
    )

    param_grid = {
        "n_estimators": n_estimators,
        "max_depth": max_depth,
        "min_samples_split": min_samples_split,
    }

    # Step 4: Train the Random Forest Regressor with hyperparameter tuning
    model = RandomForestRegressor(random_state=42)
    grid_search = GridSearchCV(
        estimator=model, param_grid=param_grid, cv=3, scoring="neg_mean_squared_error", verbose=1, n_jobs=-1
    )

    try:
        with st.spinner("Training model..."):
            grid_search.fit(X_train, y_train)
            best_model = grid_search.best_estimator_
        st.success("Model training completed successfully!")
    except Exception as e:
        st.error(f"Error during model training: {e}")
        return

    # Step 5: Make predictions and evaluate the model
    y_pred = best_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    st.write(f"### Mean Squared Error (MSE): {mse:.2f}")
    st.write(f"### R-squared (R2): {r2:.2f}")

    # Scatter plot of actual vs. predicted values
    st.write("### Actual vs. Predicted Values")
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.title("Actual vs. Predicted Values")
    st.pyplot()

    # Step 6: Display feature importance
    if st.checkbox("Show Feature Importance", key="rf_feature_importance"):
        st.write("### Feature Importance")
        feature_importance = pd.DataFrame(
            {"Feature": feature_columns, "Importance": best_model.feature_importances_}
        ).sort_values(by="Importance", ascending=False)
        st.dataframe(feature_importance)
        st.bar_chart(feature_importance.set_index("Feature"))

    # Step 7: Allow the user to download the trained model
    if st.button("Download Trained Model", key="rf_download_model"):
        model_filename = "random_forest_model.pkl"
        with open(model_filename, "wb") as file:
            pickle.dump(best_model, file)
        with open(model_filename, "rb") as file:
            st.download_button(
                label="Download Trained Model",
                data=file,
                file_name=model_filename,
                mime="application/octet-stream",
            )
        st.success(f"Model saved as {model_filename}")