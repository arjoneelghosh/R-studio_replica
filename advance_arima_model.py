import pandas as pd
import numpy as np
import streamlit as st
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox
import scipy.stats as stats

def forecast_with_adv_arima(data):
    """Perform time series forecasting using ARIMA with validation and diagnostics."""
    st.sidebar.header("Forecasting with ARIMA")

    # Debug: Print the input data
    st.write("### Input Data for Advanced ARIMA (Debug)")
    st.write(data.head())
    st.write(f"Shape of input data: {data.shape}")

    # Check and create the 'Date' column if needed
    if 'Date' not in data.columns:
        if {'Year', 'Month'}.issubset(data.columns):
            data['Date'] = pd.to_datetime(data['Year'].astype(str) + '-' + data['Month'].astype(str))
        else:
            st.error("Dataset must contain 'Year' and 'Month' columns or a 'Date' column.")
            return

    # Select target column
    target_column = st.sidebar.selectbox(
        "Select Target Column",
        options=[col for col in data.columns if col not in ['Year', 'Month', 'Date']],
        key="adv_arima_target_column"
    )

    # Debug: Print the selected target column
    st.write(f"Selected target column: {target_column}")

    try:
        # Prepare the dataset for ARIMA
        data = data.sort_values(by='Date').dropna(subset=['Date', target_column])
        data = data.rename(columns={'Date': 'ds', target_column: 'y'})
        data.set_index('ds', inplace=True)

        # Debug: Print the prepared data
        st.write("### Prepared Data for Advanced ARIMA (Debug)")
        st.write(data.head())
        st.write(f"Shape of prepared data: {data.shape}")

        # ARIMA parameters
        st.write("### ARIMA Model Configuration")
        p = st.sidebar.number_input("AR (p):", min_value=0, max_value=10, value=1, step=1, key="adv_arima_p")
        d = st.sidebar.number_input("Difference (d):", min_value=0, max_value=10, value=1, step=1, key="adv_arima_d")
        q = st.sidebar.number_input("MA (q):", min_value=0, max_value=10, value=1, step=1, key="adv_arima_q")

        # Forecast period input
        forecast_periods = st.sidebar.number_input(
            "Forecast Periods",
            min_value=1,
            max_value=365,
            value=30,
            key="adv_arima_forecast_periods"
        )

        if st.button("Run Advanced ARIMA Forecasting", key="run_adv_arima_forecasting"):
            # Fit ARIMA model
            model = ARIMA(data['y'], order=(p, d, q))
            fitted_model = model.fit()

            # Debug: Print the ARIMA model summary
            st.write("### ARIMA Model Summary (Debug)")
            st.write(fitted_model.summary())

            # Generate future dates
            freq = pd.infer_freq(data.index) or 'M'
            future_dates = pd.date_range(start=data.index[-1], periods=forecast_periods + 1, freq=freq)[1:]

            # Make predictions
            forecast_values = fitted_model.forecast(steps=forecast_periods)

            # Create forecast DataFrame
            forecast_df = pd.DataFrame({'ds': future_dates, 'yhat': forecast_values})

            # Debug: Print the forecast DataFrame
            st.write("### Forecast DataFrame (Debug)")
            st.write(forecast_df)

            # Calculate MAPE if enough data is available
            min_length = min(len(data['y']), len(forecast_values))
            actuals = data['y'][-min_length:].values
            preds = forecast_values[:min_length]
            mape = np.mean(np.abs((actuals - preds) / actuals)) * 100 if min_length > 0 and np.all(actuals != 0) else None

            # Display MAPE
            if mape is not None:
                st.write(f"### Model Accuracy (MAPE): {mape:.2f}%")
            else:
                st.warning("MAPE cannot be calculated due to zero values in the actual data.")

            # Plot actual vs forecast
            st.write("### ARIMA Forecast Plot")
            plt.figure(figsize=(12, 6))
            plt.plot(data.index, data['y'], label="Actual", marker='o', color='blue')
            plt.plot(forecast_df['ds'], forecast_df['yhat'], label="Forecast", linestyle='dashed', marker='o', color='orange')
            plt.legend()
            plt.xlabel("Date")
            plt.ylabel("Values")
            plt.title("Advanced ARIMA Forecast")
            plt.grid(True)
            st.pyplot(plt)

            # Display forecasted values
            st.write("### Forecasted Values")
            st.dataframe(forecast_df)

            # Residual diagnostics
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

            # Success message
            st.success("Advanced ARIMA forecasting completed successfully!")

    except Exception as e:
        st.error(f"Error in Advanced ARIMA forecasting: {e}")
        st.write(f"Error details: {str(e)}")