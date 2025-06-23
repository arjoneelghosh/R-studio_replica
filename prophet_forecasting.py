import pandas as pd
import streamlit as st
from prophet import Prophet
import matplotlib.pyplot as plt

def forecast_with_prophet(data):
    """Perform time series forecasting using Prophet."""
    st.sidebar.header("Forecasting with Prophet")

    # Debug: Print the input data
    st.write("### Input Data for Prophet (Debug)")
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
        key="prophet_target_column"
    )

    # Debug: Print the selected target column
    st.write(f"Selected target column: {target_column}")

    try:
        # Prepare the dataset for Prophet
        data = data.sort_values(by='Date').dropna(subset=['Date', target_column])
        data = data.rename(columns={'Date': 'ds', target_column: 'y'})

        # Debug: Print the prepared data
        st.write("### Prepared Data for Prophet (Debug)")
        st.write(data.head())
        st.write(f"Shape of prepared data: {data.shape}")

        # Forecast period input
        forecast_periods = st.sidebar.number_input(
            "Forecast Periods",
            min_value=1,
            max_value=365,
            value=30,
            key="prophet_forecast_periods"
        )

        if st.button("Run Prophet Forecasting", key="run_prophet_forecasting"):
            # Fit Prophet model
            model = Prophet()
            model.fit(data)

            # Debug: Print the Prophet model summary
            st.write("### Prophet Model Summary (Debug)")
            st.write(model)

            # Generate future dates
            future = model.make_future_dataframe(periods=forecast_periods, freq='M')

            # Make predictions
            forecast = model.predict(future)

            # Debug: Print the forecast DataFrame
            st.write("### Forecast DataFrame (Debug)")
            st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

            # Plot the forecast
            st.write("### Prophet Forecast Plot")
            fig1 = model.plot(forecast)
            st.pyplot(fig1)

            # Plot components
            st.write("### Forecast Components")
            fig2 = model.plot_components(forecast)
            st.pyplot(fig2)

            # Display forecasted values
            st.write("### Forecasted Values")
            st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

            # Success message
            st.success("Prophet forecasting completed successfully!")

    except Exception as e:
        st.error(f"Error in Prophet forecasting: {e}")
        st.write(f"Error details: {str(e)}")