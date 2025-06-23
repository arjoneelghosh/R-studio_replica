import pandas as pd
import streamlit as st
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import mean_absolute_error, mean_squared_error


def optimize_prophet(data):
    """Automatically tune Prophet parameters for best accuracy."""
    param_grid = {
        "changepoint_prior_scale": [0.001, 0.01, 0.1, 0.5],
        "seasonality_prior_scale": [0.01, 0.1, 1.0],
        "seasonality_mode": ["additive", "multiplicative"],
        "n_changepoints": [10, 25, 50],
    }
    best_mape = float("inf")
    best_params = {}

    for params in ParameterGrid(param_grid):
        model = Prophet(
            changepoint_prior_scale=params["changepoint_prior_scale"],
            seasonality_prior_scale=params["seasonality_prior_scale"],
            seasonality_mode=params["seasonality_mode"],
            n_changepoints=params["n_changepoints"],
            yearly_seasonality=True,
        )
        model.fit(data)
        future = model.make_future_dataframe(periods=30, freq="ME")
        forecast = model.predict(future)
        actuals = data["y"][-30:].values
        preds = forecast["yhat"][-30:].values
        mape = np.mean(np.abs((actuals - preds) / actuals)) * 100

        if mape < best_mape:
            best_mape = mape
            best_params = params

    return best_params, best_mape


def forecast_with_prophet(data):
    """Perform time series forecasting using Prophet."""
    st.sidebar.header("Forecasting with Prophet")

    # Date handling
    if "Date" not in data.columns:
        if "Year" in data.columns and "Month" in data.columns:
            data["Date"] = pd.to_datetime(data["Year"].astype(str) + "-" + data["Month"].astype(str))
        else:
            st.error("Dataset must contain 'Year' and 'Month' columns or a 'Date' column.")
            return

    # Target column selection
    target_column = st.sidebar.selectbox(
        "Select Target Column",
        options=[col for col in data.columns if col not in ["Year", "Month", "Date"]],
        key="prophet_target_column",
    )
    data = data.sort_values(by="Date").dropna(subset=["Date", target_column])
    data = data.rename(columns={"Date": "ds", target_column: "y"})

    # Scaling adjustments
    scale_factor = 1
    if data["y"].max() > 1e6:
        scale_factor = data["y"].max()
        data["y"] /= scale_factor
        st.warning("Target values have been scaled for better forecasting.")

    st.write("### Prophet Forecasting")
    if st.button("Run Prophet Forecasting"):
        with st.spinner("Optimizing Prophet parameters..."):
            best_params, best_mape = optimize_prophet(data)
        st.success(f"Best parameters found: {best_params}")
        st.success(f"Best MAPE: {best_mape:.2f}%")

        # Train and forecast with the best model
        model = Prophet(
            changepoint_prior_scale=best_params["changepoint_prior_scale"],
            seasonality_prior_scale=best_params["seasonality_prior_scale"],
            seasonality_mode=best_params["seasonality_mode"],
            n_changepoints=best_params["n_changepoints"],
            yearly_seasonality=True,
        )
        model.fit(data)
        future = model.make_future_dataframe(periods=30, freq="ME")
        forecast = model.predict(future)

        # Plot forecast
        st.write("### Forecast Plot")
        fig1 = model.plot(forecast)
        st.pyplot(fig1)

        # Plot trend and seasonality
        st.write("### Trend and Seasonality Components")
        fig2 = model.plot_components(forecast)
        st.pyplot(fig2)

        # Display forecasted values
        st.write("### Forecasted Values")
        st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]])

        # Evaluate model performance
        actuals = data["y"][-30:].values
        preds = forecast["yhat"][-30:].values
        mae = mean_absolute_error(actuals, preds)
        rmse = np.sqrt(mean_squared_error(actuals, preds))

        st.write("### Model Evaluation")
        st.write(f"Mean Absolute Error (MAE): {mae:.2f}")
        st.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")