import pandas as pd
import streamlit as st
from pmdarima import auto_arima
import matplotlib.pyplot as plt
import numpy as np

def forecast_with_arima(data):
    """Perform time series forecasting using ARIMA with automatic order selection and display MAPE."""
    st.sidebar.header("Forecasting with ARIMA")

    # Debug: Print the input data
    st.write("### Input Data for ARIMA (Debug)")
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
        key="arima_target_column"
    )

    # Debug: Print the selected target column
    st.write(f"Selected target column: {target_column}")

    try:
        # Prepare the dataset for ARIMA
        data = data.sort_values(by='Date').dropna(subset=['Date', target_column])
        data = data.rename(columns={'Date': 'ds', target_column: 'y'})
        data.set_index('ds', inplace=True)

        # Debug: Print the prepared data
        st.write("### Prepared Data for ARIMA (Debug)")
        st.write(data.head())
        st.write(f"Shape of prepared data: {data.shape}")

        # Forecast period input
        forecast_periods = st.sidebar.number_input(
            "Forecast Periods",
            min_value=1,
            max_value=365,
            value=30,
            key="arima_forecast_periods"
        )

        if st.button("Run ARIMA Forecasting", key="run_arima_forecasting"):
            # Auto ARIMA to find the best parameters
            model = auto_arima(data['y'], seasonal=True, m=12, trace=True, suppress_warnings=True)

            # Debug: Print the ARIMA model summary
            st.write("### ARIMA Model Summary (Debug)")
            st.write(model.summary())

            # Infer frequency or default to monthly
            freq = pd.infer_freq(data.index) or 'M'

            # Generate future dates
            future_dates = pd.date_range(start=data.index[-1], periods=forecast_periods + 1, freq=freq)[1:]

            # Make predictions
            forecast_values = model.predict(n_periods=forecast_periods)

            # Debug: Print the forecast values
            st.write("### Forecast Values (Debug)")
            st.write(forecast_values)

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
            plt.title("ARIMA Forecast")
            plt.grid(True)
            st.pyplot(plt)

            # Display forecasted values
            st.write("### Forecasted Values")
            st.dataframe(forecast_df)

            # Success message
            st.success("ARIMA forecasting completed successfully!")

    except Exception as e:
        st.error(f"Error in ARIMA forecasting: {e}")
        st.write(f"Error details: {str(e)}")