import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.arima.model import ARIMA
from prophet_forecasting import Prophet

# Streamlit App Title
st.title("Forecasting Tool")

# Sidebar for File Upload
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Load Data
    data = pd.read_csv(uploaded_file)

    # Ensure 'Date' column is correctly formatted as datetime
    try:
        data['Date'] = pd.to_datetime(data['Year'].astype(str) + '-' + data['Quarter'].str[1:] + '-01', format='%Y-%m-%d')
    except Exception as e:
        st.error(f"Error in date conversion: {e}")

    # Explicitly convert 'Date' to string to avoid serialization issues
    try:
        data['Date'] = data['Date'].astype(str)  # Convert to string format
    except Exception as e:
        st.error(f"Error in converting Date to string: {e}")

    st.write("### Data Preview")
    st.dataframe(data)

    # Sidebar for Data Preprocessing
    st.sidebar.header("Data Preprocessing")
    columns = st.sidebar.multiselect("Select columns to use", data.columns)

    if st.sidebar.checkbox("Fill missing values"):
        fill_value = st.sidebar.number_input("Fill missing values with:")
        data = data.fillna(fill_value)

    st.write("### Preprocessed Data")
    st.dataframe(data[columns])

    # Encode categorical columns
    categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
    for col in categorical_cols:
        if col != 'Date':  # Avoid encoding the 'Date' column
            data = pd.get_dummies(data, columns=[col], drop_first=True)

    st.write("### Preprocessed Data with Encoded Categorical Variables")
    st.dataframe(data)

    # Sidebar for Exploratory Data Analysis
    st.sidebar.header("Exploratory Data Analysis")
    if st.sidebar.button("Show Data Summary"):
        st.write(data.describe())

    if st.sidebar.checkbox("Correlation Heatmap"):
        st.write("### Correlation Heatmap")

        # Select only numeric columns for correlation
        numeric_data = data.select_dtypes(include=[np.number])

        # Generate the correlation heatmap
        if numeric_data.empty:
            st.write("No numeric columns found for correlation analysis.")
        else:
            fig, ax = plt.subplots()
            sns.heatmap(numeric_data.corr(), annot=True, ax=ax)
            st.pyplot(fig)

    # Sidebar for Model Training
    st.sidebar.header("Train Model")
    if st.sidebar.button("Train Forecasting Model"):
        target = st.sidebar.selectbox("Select target variable", columns)
        features = [col for col in columns if col != target and col != 'Date']  # Exclude 'Date' from features

        # Convert 'Date' column to numeric for model if required
        if 'Date' in features:
            features.remove('Date')
            features.append('Date_numeric')

        try:
            X_train, X_test, y_train, y_test = train_test_split(
                data[features], data[target], test_size=0.2, random_state=42
            )

            model = RandomForestRegressor(random_state=42)
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            mae = mean_absolute_error(y_test, predictions)

            st.write(f"### Model Performance")
            st.write(f"Mean Absolute Error: {mae}")
        except Exception as e:
            st.error(f"Error in model training: {e}")

    # Sidebar for Time Series Forecasting
    st.sidebar.header("Forecasting")
    
    # ARIMA Forecasting
if st.sidebar.button("Forecast with ARIMA"):
    time_column = st.sidebar.selectbox("Select time column", data.columns)
    target = st.sidebar.selectbox("Select target variable", columns)

    try:
        # Ensure target column is numeric and handle errors if conversion fails
        data[target] = pd.to_numeric(data[target], errors='coerce')  # Convert non-numeric to NaN
        
        # Drop rows where target or time column has NaN values
        data_cleaned = data.dropna(subset=[target, time_column])

        # Check if there are enough data points after cleaning
        if len(data_cleaned) < 2:
            st.error("Not enough data points to train the ARIMA model. Please check the data.")
        else:
            # Ensure the 'time_column' is in datetime format
            data_cleaned[time_column] = pd.to_datetime(data_cleaned[time_column])

            # ARIMA Model
            model = ARIMA(data_cleaned[target], order=(1, 1, 1))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=10)

            # Plot the ARIMA forecast
            st.write("### ARIMA Forecast")
            fig, ax = plt.subplots()
            ax.plot(data_cleaned[time_column], data_cleaned[target], label="Original Data")
            ax.plot(pd.date_range(data_cleaned[time_column].iloc[-1], periods=10, freq='D'), forecast, label="Forecast")
            ax.legend()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Error in ARIMA forecasting: {e}")


    # Prophet Forecasting
    if st.sidebar.button("Forecast with Prophet"):
        time_column = st.sidebar.selectbox("Select time column", data.columns)
        target = st.sidebar.selectbox("Select target variable", columns)

        try:
            df = data[[time_column, target]].rename(columns={time_column: "ds", target: "y"})
            model = Prophet()
            model.fit(df)
            future = model.make_future_dataframe(periods=10)
            forecast = model.predict(future)

            st.write("### Prophet Forecast")
            fig, ax = plt.subplots()
            ax.plot(df['ds'], df['y'], label="Original Data")
            ax.plot(forecast['ds'], forecast['yhat'], label="Forecast")
            ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error in Prophet forecasting: {e}")
