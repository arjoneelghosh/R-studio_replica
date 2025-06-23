import streamlit as st
from data_loader import load_data
from data_editor import edit_data
from preprocessing import preprocess_data
from visualization import display_eda
from model_training import train_model
from forecasting import forecast_with_arima                              #BETTER than hello_cache button
from prophet_forecasting import forecast_with_prophet                                            
from advance_arima_model import forecast_with_adv_arima
from advance_prophet_model import forecast_with_adv_prophet

# Main app title
st.title("Forecasting Tool")

# File upload and data loading
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Load data only when it's uploaded
    data = load_data(uploaded_file)

    # Save original data for safety (only on first upload)
    if "original_data" not in st.session_state:
        st.session_state.original_data = data.copy()

    # Initialize edited_data in session state (if not already initialized)
    if "edited_data" not in st.session_state:
        st.session_state.edited_data = data.copy()

    # Display file and column information in the sidebar
    st.sidebar.subheader("Column Names")
    st.sidebar.write(data.columns.tolist())

    # Add data editing feature
    st.sidebar.header("Data Editing Options")
    enable_edit = st.sidebar.checkbox("Edit Data")

    # Allow the user to edit data interactively
    if enable_edit:
        st.session_state.edited_data = edit_data(st.session_state.edited_data)

    # After editing, use the edited data throughout the pipeline
    data = st.session_state.edited_data

    # Validate the dataset (after editing or initial load)
    if data.empty:
        st.error("The dataset is empty. Please upload a valid dataset.")
    else:
        # Proceed with the edited data
        st.write("### Final Dataset")
        st.dataframe(data)  # Show the edited dataset for confirmation

        # Preprocess the edited data
        preprocessed_data = preprocess_data(data)

        # Perform EDA
        display_eda(preprocessed_data)

        # Train the model using the preprocessed data
        train_model(preprocessed_data)

        # ARIMA Forecasting Section
        st.write("### ARIMA Forecasting")
        if st.button("Run ARIMA Forecasting", key="run_arima"):
            forecast_with_arima(preprocessed_data)

        # Advanced ARIMA Forecasting Section
        st.write("### Advanced ARIMA Forecasting")
        if st.button("Run Advanced ARIMA Forecasting", key="run_adv_arima"):
            forecast_with_adv_arima(preprocessed_data)

        # Prophet Forecasting Section
        st.write("### Prophet Forecasting")
        if st.button("Run Prophet Forecasting", key="run_prophet"):
            forecast_with_prophet(preprocessed_data)

        # Advanced Prophet Forecasting Section
        st.write("### Advanced Prophet Forecasting")
        if st.button("Run Advanced Prophet Forecasting", key="run_adv_prophet"):
            forecast_with_adv_prophet(preprocessed_data)
else:
    st.info("Please upload a CSV file to get started.")