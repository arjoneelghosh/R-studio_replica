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

    # Missing value analysis
    if st.sidebar.checkbox("Show Missing Value Analysis", key="eda_missing_values"):
        st.write("### Missing Value Analysis")
        missing_values = data.isnull().sum()
        missing_df = pd.DataFrame({"Column": missing_values.index, "Missing Values": missing_values.values})
        st.dataframe(missing_df)
        if missing_values.sum() > 0:
            st.bar_chart(missing_values)
        else:
            st.info("No missing values found.")

    # Pair plot
    if st.sidebar.checkbox("Show Pair Plot", key="eda_pair_plot"):
        numeric_columns = data.select_dtypes(include=["number"]).columns.tolist()
        if len(numeric_columns) < 2:
            st.warning("Not enough numeric columns to generate a pair plot.")
        else:
            selected_columns = st.multiselect(
                "Select Columns for Pair Plot", numeric_columns, default=numeric_columns, key="pair_plot_columns"
            )
            if selected_columns:
                st.write("### Pair Plot")
                sns.pairplot(data[selected_columns])
                st.pyplot()
                st.success("Pair plot generated successfully!")

    # Correlation heatmap
    if st.sidebar.checkbox("Show Correlation Heatmap", key="eda_corr_heatmap"):
        st.write("### Correlation Heatmap")
        numeric_columns = data.select_dtypes(include=["number"]).columns.tolist()
        if len(numeric_columns) < 2:
            st.warning("Not enough numeric columns to compute correlation.")
        else:
            corr_matrix = data[numeric_columns].corr()
            plt.figure(figsize=(10, 6))
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", cbar=True, fmt=".2f", linewidths=0.5)
            st.pyplot()
            st.success("Correlation heatmap computed successfully!")

    # Column distributions
    if st.sidebar.checkbox("Show Column Distributions", key="eda_column_distributions"):
        st.write("### Column Distributions")
        selected_column = st.selectbox("Select a Column", data.columns, key="eda_column_selector")
        if pd.api.types.is_numeric_dtype(data[selected_column]):
            plot_type = st.radio("Choose Plot Type", ["Histogram", "Box Plot"], key="eda_plot_type")
            if plot_type == "Histogram":
                sns.histplot(data[selected_column], kde=True, bins=30, color="blue")
                plt.title(f"Distribution of {selected_column}")
                st.pyplot()
            elif plot_type == "Box Plot":
                sns.boxplot(x=data[selected_column], color="blue")
                plt.title(f"Box Plot of {selected_column}")
                st.pyplot()
        elif pd.api.types.is_categorical_dtype(data[selected_column]) or data[selected_column].dtype == "object":
            plot_type = st.radio("Choose Plot Type", ["Count Plot", "Pie Chart"], key="eda_plot_type")
            if plot_type == "Count Plot":
                sns.countplot(y=data[selected_column], palette="viridis")
                plt.title(f"Count Plot of {selected_column}")
                st.pyplot()
            elif plot_type == "Pie Chart":
                value_counts = data[selected_column].value_counts()
                plt.figure(figsize=(6, 6))
                plt.pie(value_counts, labels=value_counts.index, autopct="%1.1f%%", startangle=90)
                plt.title(f"Pie Chart of {selected_column}")
                st.pyplot()
        else:
            st.warning("Selected column type is not supported for visualization.")