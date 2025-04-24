import pandas as pd
from datetime import datetime

def clean_data(input_path, output_path):
    """
    Function to clean the crime dataset.

    Parameters:
    input_path (str): Path to the raw input CSV file.
    output_path (str): Path where the cleaned CSV will be saved.
    """
    print(f"Loading data from: {input_path}")
    df = pd.read_csv(input_path)
    print(f"Initial shape: {df.shape}")

    # Function to safely convert date columns
    def convert_date_column(df, column_name, errors='coerce'):
        if column_name in df.columns:
            df[column_name] = pd.to_datetime(df[column_name], errors=errors, dayfirst=True)
        return df

    # Convert date columns
    date_columns = ['Date Reported', 'Date of Occurrence', 'Date Case Closed']
    for column in date_columns:
        df = convert_date_column(df, column)

    # Convert time column safely (first parse, then extract time)
    if 'Time of Occurrence' in df.columns:
        df['Time of Occurrence'] = pd.to_datetime(df['Time of Occurrence'], errors='coerce', dayfirst=True)
        df['Time of Occurrence'] = df['Time of Occurrence'].dt.time

    # Drop rows with missing critical values in 'Date of Occurrence' and 'City'
    if 'Date of Occurrence' in df.columns and 'City' in df.columns:
        df = df.dropna(subset=['Date of Occurrence', 'City'])

    # Handle missing values for categorical columns
    categorical_columns = ['Crime Description', 'Crime Domain', 'City', 'Weapon Used', 'Victim Gender']
    default_values = {
        'Crime Description': 'Unknown',
        'Crime Domain': 'Unknown',
        'City': 'Unknown',
        'Weapon Used': 'Unknown',
        'Victim Gender': 'Unknown'
    }

    for col in categorical_columns:
        if col in df.columns:
            df[col] = df[col].fillna(default_values[col])

    # Handle numeric fields
    if 'Victim Age' in df.columns:
        df['Victim Age'] = df['Victim Age'].fillna(df['Victim Age'].mean())

    # Handle missing values in 'Case Closed' column
    if 'Case Closed' in df.columns:
        df['Case Closed'] = df['Case Closed'].fillna('No')

    # Feature Engineering from dates
    if 'Date of Occurrence' in df.columns:
        df['Year'] = df['Date of Occurrence'].dt.year
        df['Month'] = df['Date of Occurrence'].dt.month
        df['Day of Week'] = df['Date of Occurrence'].dt.day_name()

    if 'Date Case Closed' in df.columns and 'Date of Occurrence' in df.columns:
        df['Closure Time (Days)'] = (df['Date Case Closed'] - df['Date of Occurrence']).dt.days
        df['Closure Time (Days)'] = df['Closure Time (Days)'].fillna(0).astype(int)

    # Remove duplicates if any exist
    df = df.drop_duplicates()

    # Save cleaned data
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to: {output_path}")
    print(f"Final shape: {df.shape}")

if __name__ == "__main__":
    clean_data("data/raw/crime_dataset_india.csv", "data/processed/cleaned_crime_data_final.csv")
