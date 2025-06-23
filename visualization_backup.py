import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def display_eda(data):
    """Perform and display exploratory data analysis."""
    st.header("Exploratory Data Analysis")

    # Display basic statistics
    st.write("### Data Statistics")
    st.write(data.describe())

    # Add a toggle for missing value analysis
    if st.sidebar.checkbox("Show Missing Value Analysis", key="eda_missing_values"):
        st.write("### Missing Value Analysis")
        missing_values = data.isnull().sum()
        missing_df = pd.DataFrame({"Column": missing_values.index, "Missing Values": missing_values.values})
        st.dataframe(missing_df)

    # Add a toggle for pair plots
    if st.sidebar.checkbox("Show Pair Plot", key="eda_pair_plot"):
        numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
        if len(numeric_columns) < 2:
            st.warning("Not enough numeric columns to generate a pair plot.")
        else:
            selected_columns = st.multiselect("Select Columns for Pair Plot", numeric_columns, default=numeric_columns, key="pair_plot_columns")
            if selected_columns:
                st.write("### Pair Plot")
                sns.pairplot(data[selected_columns])
                st.pyplot()

    # Add correlation heatmap
    if st.sidebar.checkbox("Show Correlation Heatmap", key="eda_corr_heatmap"):
        st.write("### Correlation Heatmap")
        numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
        if len(numeric_columns) < 2:
            st.warning("Not enough numeric columns to compute correlation.")
        else:
            corr_matrix = data[numeric_columns].corr()
            plt.figure(figsize=(10, 6))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', cbar=True, fmt=".2f", linewidths=0.5)
            st.pyplot()

    # Allow visualization of individual column distributions
    if st.sidebar.checkbox("Show Column Distributions", key="eda_column_distributions"):
        st.write("### Column Distributions")
        selected_column = st.selectbox("Select a Column", data.columns, key="eda_column_selector")
        if pd.api.types.is_numeric_dtype(data[selected_column]):
            sns.histplot(data[selected_column], kde=True, bins=30, color='blue')
            plt.title(f"Distribution of {selected_column}")
            st.pyplot()
        elif pd.api.types.is_categorical_dtype(data[selected_column]) or data[selected_column].dtype == 'object':
            sns.countplot(y=data[selected_column], palette='viridis')
            plt.title(f"Count Plot of {selected_column}")
            st.pyplot()
        else:
            st.warning("Selected column type is not supported for visualization.")
