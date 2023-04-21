import os
import pandas as pd

def concat():
    # get a list of all the CSV files in the directory
    csv_files = [f for f in os.listdir('dataset') if f.endswith('.csv') and f != 'concatenated_dataset.csv']

    # loop through the list and concatenate the dataframes
    concatenated_df = pd.DataFrame()
    for csv_file in csv_files:
        df = pd.read_csv('dataset/'+ csv_file, encoding='cp1252')
        concatenated_df = pd.concat([concatenated_df, df])

    # write the concatenated dataframe to a new CSV file
    concatenated_df.to_csv('dataset/concatenated_dataset.csv', index=False)