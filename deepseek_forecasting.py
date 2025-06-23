import pandas as pd
import streamlit as st
import joblib  # or the appropriate library for loading your model
import numpy as np
import matplotlib.pyplot as plt

def forecast_with_deepseek(data):
    """Perform time series forecasting using the DeepSeek model."""
    st.sidebar.header("Forecasting with DeepSeek")

    # Debug: Print the input data
    st.write("### Input Data for DeepSeek (Debug)")
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
        key="deepseek_target_column"
    )

    # Debug: Print the selected target column
    st.write(f"Selected target column: {target_column}")

    try:
        # Prepare the dataset for DeepSeek
        data = data.sort_values(by='Date').dropna(subset=['Date', target_column])
        data = data.rename(columns={'Date': 'ds', target_column: 'y'})
        data.set_index('ds', inplace=True)

        # Debug: Print the prepared data
        st.write("### Prepared Data for DeepSeek (Debug)")
        st.write(data.head())
        st.write(f"Shape of prepared data: {data.shape}")

        # Load the DeepSeek model
        model = joblib.load("deepseek_model.pkl")  # Replace with your model file

        # Forecast period input
        forecast_periods = st.sidebar.number_input(
            "Forecast Periods",
            min_value=1,
            max_value=365,
            value=30,
            key="deepseek_forecast_periods"
        )

        if st.button("Run DeepSeek Forecasting", key="run_deepseek_forecasting"):
            # Prepare input for the model
            X = data[['y']].values  # Replace with the appropriate input format for your model

            # Make predictions
            predictions = model.predict(X)  # Replace with the appropriate prediction method

            # Generate future dates
            freq = pd.infer_freq(data.index) or 'M'
            future_dates = pd.date_range(start=data.index[-1], periods=forecast_periods + 1, freq=freq)[1:]

            # Create forecast DataFrame
            forecast_df = pd.DataFrame({'ds': future_dates, 'yhat': predictions[:forecast_periods]})

            # Debug: Print the forecast DataFrame
            st.write("### Forecast DataFrame (Debug)")
            st.write(forecast_df)

            # Plot actual vs forecast
            st.write("### DeepSeek Forecast Plot")
            plt.figure(figsize=(12, 6))
            plt.plot(data.index, data['y'], label="Actual", marker='o', color='blue')
            plt.plot(forecast_df['ds'], forecast_df['yhat'], label="Forecast", linestyle='dashed', marker='o', color='orange')
            plt.legend()
            plt.xlabel("Date")
            plt.ylabel("Values")
            plt.title("DeepSeek Forecast")
            plt.grid(True)
            st.pyplot(plt)

            # Display forecasted values
            st.write("### Forecasted Values")
            st.dataframe(forecast_df)

            # Success message
            st.success("DeepSeek forecasting completed successfully!")

    except Exception as e:
        st.error(f"Error in DeepSeek forecasting: {e}")
        st.write(f"Error details: {str(e)}")