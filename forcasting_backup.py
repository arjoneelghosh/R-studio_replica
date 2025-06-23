import pandas as pd
import numpy as np
import streamlit as st
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox
import scipy.stats as stats

def forecast_with_arima(data):
    """Perform time series forecasting using ARIMA with validation and diagnostics."""
    st.sidebar.header("Forecasting with ARIMA")

    # Step 1: Combine Year and Month into a datetime column if needed
    if 'Date' not in data.columns:
        if 'Year' in data.columns and 'Month' in data.columns:
            data['Date'] = pd.to_datetime(data['Year'].astype(str) + '-' + data['Month'].astype(str))
        else:
            st.error("Dataset must contain 'Year' and 'Month' columns or a 'Date' column.")
            return

    # Step 2: Allow user to select the target column
    target_column = st.sidebar.selectbox(
        "Select Target Column",
        options=[col for col in data.columns if col not in ['Year', 'Month', 'Date']],
        key="arima_target_column"
    )

    # Step 3: Validate the target column and preprocess
    try:
        data = data.sort_values(by='Date').dropna(subset=['Date', target_column])
        data.set_index('Date', inplace=True)
        data.index = data.index.to_period('M').to_timestamp()  # Explicitly set frequency to month-start
        target_series = data[target_column]
    except Exception as e:
        st.error(f"Data preparation error: {e}")
        return

    # Ensure target column is numerical
    if not np.issubdtype(target_series.dtype, np.number):
        st.error(f"The target column '{target_column}' must contain numerical data.")
        return

    scale_factor = 1
    if target_series.max() > 1e6:
        scale_factor = target_series.max()
        target_series /= scale_factor
        st.warning("Target values have been scaled for better ARIMA performance.")

    # Step 4: ARIMA parameters
    st.write("### ARIMA Model Configuration")
    p = st.sidebar.number_input("AR (p):", min_value=0, max_value=10, value=1, step=1)
    d = st.sidebar.number_input("Difference (d):", min_value=0, max_value=10, value=1, step=1)
    q = st.sidebar.number_input("MA (q):", min_value=0, max_value=10, value=1, step=1)

    # Forecast periods
    forecast_periods = st.sidebar.slider(
        "Number of periods to forecast",
        min_value=1,
        max_value=365,
        value=30,
        key="arima_forecast_periods"
    )

    try:
        # Step 5: Fit ARIMA model
        model = ARIMA(target_series, order=(p, d, q))
        fitted_model = model.fit()
        st.write(f"Fitted ARIMA Order: ({p}, {d}, {q})")

        # Step 6: Forecast future values
        forecast = fitted_model.forecast(steps=forecast_periods)
        forecast_index = pd.date_range(start=target_series.index[-1], periods=forecast_periods + 1, freq='MS')[1:]
        forecast_df = pd.DataFrame({"Forecast": forecast * scale_factor}, index=forecast_index)

        # Step 7: Plot the forecast
        st.write("### ARIMA Forecast Plot")
        plt.figure(figsize=(10, 6))
        plt.plot(target_series * scale_factor, label="Actual Data")
        plt.plot(forecast_df.index, forecast_df['Forecast'], label="Forecast", color="orange")
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel(target_column)
        plt.title("ARIMA Forecast")
        st.pyplot(plt)

        # Step 8: Display forecasted values
        st.write("### Forecasted Values")
        st.dataframe(forecast_df)

        # Step 9: Evaluate model performance
        if len(target_series) > forecast_periods:
            actuals = target_series[-forecast_periods:]
            forecasted = forecast[:len(actuals)] * scale_factor
            mape = mean_absolute_percentage_error(actuals, forecasted)
            st.write(f"### Mean Absolute Percentage Error (MAPE): {mape:.2f}%")

        # Step 10: Residual diagnostics
        diagnostics_enabled = st.sidebar.checkbox("Enable Residual Diagnostics", value=True)
        if diagnostics_enabled:
            st.write("### Residual Diagnostics")
            residuals = fitted_model.resid

            # Residual Plot
            st.write("#### Residual Plot")
            plt.figure(figsize=(10, 6))
            plt.plot(residuals, label="Residuals")
            plt.axhline(y=0, color="red", linestyle="--")
            plt.title("Residuals Plot")
            plt.xlabel("Time")
            plt.ylabel("Residuals")
            plt.legend()
            st.pyplot(plt)

            # Histogram of Residuals
            st.write("#### Histogram of Residuals")
            plt.figure(figsize=(8, 5))
            plt.hist(residuals, bins=30, edgecolor="black")
            plt.title("Histogram of Residuals")
            plt.xlabel("Residual Value")
            plt.ylabel("Frequency")
            st.pyplot(plt)

            # ACF Plot of Residuals
            st.write("#### ACF of Residuals")
            plot_acf(residuals, lags=30)
            plt.title("ACF of Residuals")
            st.pyplot(plt)

            # Q-Q Plot
            st.write("#### Q-Q Plot")
            plt.figure(figsize=(8, 6))
            stats.probplot(residuals, dist="norm", plot=plt)
            plt.title("Q-Q Plot of Residuals")
            st.pyplot(plt)

            # Ljung-Box Test
            st.write("#### Ljung-Box Test")
            lb_test = acorr_ljungbox(residuals, lags=[10], return_df=True)
            st.write(lb_test)

            # Shapiro-Wilk Test
            st.write("#### Shapiro-Wilk Test")
            stat, p = stats.shapiro(residuals)
            st.write(f"Shapiro-Wilk Test: Statistic={stat:.4f}, p-value={p:.4f}")
            if p > 0.05:
                st.write("Residuals appear to follow a normal distribution.")
            else:
                st.write("Residuals do not appear to follow a normal distribution.")

    except Exception as e:
        st.error(f"Error in ARIMA forecasting: {e}")
