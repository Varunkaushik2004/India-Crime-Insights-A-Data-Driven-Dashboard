import os
import pandas as pd
from datetime import datetime

def clean_individual_df(df):
    # Convert date columns
    date_columns = ['Date Reported', 'Date of Occurrence', 'Date Case Closed']
    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors='coerce', dayfirst=True)

    if 'Time of Occurrence' in df.columns:
        df['Time of Occurrence'] = pd.to_datetime(df['Time of Occurrence'], errors='coerce', dayfirst=True)
        df['Time of Occurrence'] = df['Time of Occurrence'].dt.time

    if 'Date of Occurrence' in df.columns and 'City' in df.columns:
        df = df.dropna(subset=['Date of Occurrence', 'City'])

    # Fill categorical columns
    default_values = {
        'Crime Description': 'Unknown',
        'Crime Domain': 'Unknown',
        'City': 'Unknown',
        'Weapon Used': 'Unknown',
        'Victim Gender': 'Unknown'
    }
    for col, default in default_values.items():
        if col in df.columns:
            df[col] = df[col].fillna(default)

    if 'Victim Age' in df.columns:
        df['Victim Age'] = df['Victim Age'].fillna(df['Victim Age'].mean())

    if 'Case Closed' in df.columns:
        df['Case Closed'] = df['Case Closed'].fillna('No')

    if 'Date of Occurrence' in df.columns:
        df['Year'] = df['Date of Occurrence'].dt.year
        df['Month'] = df['Date of Occurrence'].dt.month
        df['Day of Week'] = df['Date of Occurrence'].dt.day_name()

    if 'Date Case Closed' in df.columns and 'Date of Occurrence' in df.columns:
        df['Closure Time (Days)'] = (df['Date Case Closed'] - df['Date of Occurrence']).dt.days
        df['Closure Time (Days)'] = df['Closure Time (Days)'].fillna(0).astype(int)

    df = df.drop_duplicates()
    return df


def merge_and_clean_all(input_folder, output_file):
    all_dfs = []

    for file in os.listdir(input_folder):
        if file.endswith(".csv"):
            path = os.path.join(input_folder, file)
            print(f"Processing: {file}")
            raw_df = pd.read_csv(path)
            cleaned_df = clean_individual_df(raw_df)
            all_dfs.append(cleaned_df)

    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df.drop_duplicates(inplace=True)
        combined_df.to_csv(output_file, index=False)
        print(f"Merged and cleaned data saved to: {output_file}")
        print(f"Total combined rows: {combined_df.shape[0]}")
    else:
        print("No CSV files found to process.")


if __name__ == "__main__":
    merge_and_clean_all("data/raw", "data/processed/cleaned_crime_data_final.csv")
