import pandas as pd
import os

# Set the directory containing the CSV files
input_directory = 'C:/Users/Vishal/OneDrive/Desktop/New folder/'

# Initialize an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Loop through all CSV files in the specified directory
for filename in os.listdir(input_directory):
    if filename.endswith(".csv"):
        # Load each CSV file into a DataFrame
        file_path = os.path.join(input_directory, filename)
        data = pd.read_csv(file_path)
        
        # Concatenate the data to the merged_data DataFrame
        merged_data = pd.concat([merged_data, data], ignore_index=True)

# Specify the output file path for the merged CSV
output_file = 'C:/Users/Vishal/OneDrive/Desktop/New folder/merged_data.csv'

# Save the merged data to a new CSV file
merged_data.to_csv(output_file, index=False)

print(f'Merged data saved to {output_file}')
