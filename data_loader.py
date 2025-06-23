import pandas as pd
import streamlit as st


def load_data(uploaded_file, encoding="utf-8"):
    """
    Loads data from an uploaded file.

    Supports CSV, Excel (.xlsx), and JSON formats.

    Parameters:
        uploaded_file: Uploaded file object.
        encoding (str): File encoding (default is 'utf-8').

    Returns:
        pd.DataFrame: Loaded dataset or None if an error occurs.
    """
    try:
        # Determine file type based on the extension
        file_name = uploaded_file.name
        if file_name.endswith(".csv"):
            data = pd.read_csv(uploaded_file, encoding=encoding)
        elif file_name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)
        elif file_name.endswith(".json"):
            data = pd.read_json(uploaded_file)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV, Excel (.xlsx), or JSON file.")

        # Display success message with dataset information
        st.success(
            f"File loaded successfully! Dataset contains {data.shape[0]} rows and {data.shape[1]} columns."
        )
        st.write("### Dataset Preview")
        st.dataframe(data.head())  # Show the first 5 rows for quick inspection

        return data

    except ValueError as ve:
        st.error(str(ve))
        return None
    except UnicodeDecodeError:
        st.error("File encoding issue. Please check the encoding (default is UTF-8).")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the file: {e}")
        return None