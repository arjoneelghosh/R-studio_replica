import pandas as pd
import streamlit as st


def preprocess_data(data):
    """Preprocess the uploaded data, including missing value handling and encoding."""
    # Sidebar options for preprocessing
    st.sidebar.header("Data Preprocessing")

    # Column selection
    columns = st.sidebar.multiselect("Select columns to use", data.columns, default=data.columns)
    data = data[columns]  # Filter data based on selected columns

    # Missing value handling
    st.sidebar.subheader("Missing Value Handling")
    if st.sidebar.checkbox("Handle missing values"):
        missing_value_option = st.sidebar.selectbox(
            "Choose an option:",
            ["Fill with a value", "Drop rows with missing values", "Drop columns with missing values"],
        )
        if missing_value_option == "Fill with a value":
            fill_value = st.sidebar.number_input("Fill missing values with:", value=0)
            data = data.fillna(fill_value)
            st.success("Missing values filled successfully!")
        elif missing_value_option == "Drop rows with missing values":
            data = data.dropna(axis=0)
            st.success("Rows with missing values dropped successfully!")
        elif missing_value_option == "Drop columns with missing values":
            data = data.dropna(axis=1)
            st.success("Columns with missing values dropped successfully!")

    # Display preprocessed data
    st.write("### Preprocessed Data")
    st.dataframe(data)

    # Categorical encoding
    st.sidebar.subheader("Categorical Encoding")
    categorical_cols = data.select_dtypes(include=["object"]).columns.tolist()
    if "Date" in categorical_cols:
        categorical_cols.remove("Date")  # Exclude Date column from encoding

    if categorical_cols:
        encoding_option = st.sidebar.selectbox(
            "Choose encoding method:", ["One-Hot Encoding", "Label Encoding"]
        )
        if encoding_option == "One-Hot Encoding":
            data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)
            st.success("Categorical variables encoded using One-Hot Encoding!")
        elif encoding_option == "Label Encoding":
            from sklearn.preprocessing import LabelEncoder

            le = LabelEncoder()
            for col in categorical_cols:
                data[col] = le.fit_transform(data[col])
            st.success("Categorical variables encoded using Label Encoding!")
    else:
        st.info("No categorical columns to encode.")

    # Display encoded data
    st.write("### Data with Encoded Categorical Variables")
    st.dataframe(data)

    return data