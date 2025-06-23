import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.arima.model import ARIMA

# Streamlit App Title
st.title("Forecasting Tool")

# Sidebar for File Upload
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Load data
    try:
        data = pd.read_csv(uploaded_file)
        st.write("### Data Preview")
        st.dataframe(data)
    except Exception as e:
        st.error(f"Error loading file: {e}")

    # Ensure 'Date' column creation if 'Year' and 'Quarter' are present
    if 'Year' in data.columns and 'Quarter' in data.columns:
        try:
            data['Date'] = pd.to_datetime(
                data['Year'].astype(str) + '-' + data['Quarter'].str[1:] + '-01',
                format='%Y-%m-%d'
            )
            st.success("Date column created successfully.")
        except Exception as e:
            st.error(f"Error creating Date column: {e}")

    # Convert 'Date' column to string for display
    if 'Date' in data.columns:
        data['Date'] = data['Date'].astype(str)

    # Sidebar for Data Preprocessing
    st.sidebar.header("Data Preprocessing")
    columns = st.sidebar.multiselect("Select columns to use", data.columns, default=data.columns)

    # Fill missing values if checked
    if st.sidebar.checkbox("Fill missing values"):
        fill_value = st.sidebar.number_input("Fill missing values with:", value=0)
        data = data.fillna(fill_value)

    # Display preprocessed data
    st.write("### Preprocessed Data")
    st.dataframe(data[columns])

    # Encode categorical variables (excluding 'Date')
    categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
    if 'Date' in categorical_cols:
        categorical_cols.remove('Date')

    data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)
    st.write("### Data with Encoded Categorical Variables")
    st.dataframe(data)

    # Sidebar for Exploratory Data Analysis (EDA)
    st.sidebar.header("Exploratory Data Analysis")

    if st.sidebar.button("Show Data Summary"):
        st.write(data.describe())

    if st.sidebar.checkbox("Correlation Heatmap"):
        numeric_data = data.select_dtypes(include=[np.number])
        if numeric_data.empty:
            st.write("No numeric columns available for correlation analysis.")
        else:
            st.write("### Correlation Heatmap")
            fig, ax = plt.subplots()
            sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

    # Sidebar for Model Training
    st.sidebar.header("Train Model")
    if st.sidebar.button("Train Forecasting Model"):
        target = st.sidebar.selectbox("Select target variable", columns)
        features = [col for col in columns if col != target and col != 'Date']

        try:
            X_train, X_test, y_train, y_test = train_test_split(
                data[features], data[target], test_size=0.2, random_state=42
            )

            model = RandomForestRegressor(random_state=42)
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            mae = mean_absolute_error(y_test, predictions)

            st.write("### Model Performance")
            st.write(f"Mean Absolute Error: {mae}")
        except KeyError as e:
            st.error(f"Missing column in data: {e}")
        except Exception as e:
            st.error(f"Error in model training: {e}")

    # Sidebar for Time Series Forecasting
    st.sidebar.header("Forecasting")

    # ARIMA Forecasting
    if st.sidebar.button("Forecast with ARIMA"):
        time_column = st.sidebar.selectbox("Select time column", data.columns)
        target = st.sidebar.selectbox("Select target variable", columns)

        try:
            # Ensure time_column is in datetime format
            data[time_column] = pd.to_datetime(data[time_column], errors='coerce')
            data_cleaned = data.dropna(subset=[target, time_column])

            if data_cleaned.empty or len(data_cleaned) < 10:
                st.error("Not enough data points to train ARIMA. Ensure at least 10 data points are available.")
            else:
                # Set time_column as index
                data_cleaned = data_cleaned.sort_values(by=time_column).set_index(time_column)

                # Train ARIMA model
                model = ARIMA(data_cleaned[target], order=(1, 1, 1))
                model_fit = model.fit()

                # Forecast future values
                forecast = model_fit.forecast(steps=10)
                future_dates = pd.date_range(start=data_cleaned.index[-1], periods=10, freq='D')

                # Plot results
                st.write("### ARIMA Forecast")
                fig, ax = plt.subplots()
                ax.plot(data_cleaned.index, data_cleaned[target], label="Original Data")
                ax.plot(future_dates, forecast, label="Forecast", color='orange')
                ax.set_title("ARIMA Forecast")
                ax.set_xlabel("Date")
                ax.set_ylabel(target)
                ax.legend()
                st.pyplot(fig)

        except Exception as e:
            st.error(f"Error in ARIMA forecasting: {e}")
