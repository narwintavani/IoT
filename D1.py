import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the Excel file
file_path = 'C:/Users/psaki/Desktop/MAI/650/Project/EPL 650 Project.xlsx'  # Replace with the path to your Excel file

# Read the names of the sheets in the Excel file
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names

# Process each sheet
for sheet_name in sheet_names:
    # Read the data from the current sheet
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Check if the required columns exist in the sheet
    if 'DIO SEND' in df.columns and 'DAO SEND' in df.columns:
        # Exclude the last row (summation row) from the data
        df = df.iloc[:-1]

        # Replace NaN values with 0 and convert to integer
        df['DIO SEND'] = df['DIO SEND'].fillna(0).astype(int)
        df['DAO SEND'] = df['DAO SEND'].fillna(0).astype(int)

        # Convert float values in time_column to strings
        df['TIME'] = df['TIME'].astype(str)

        # Extract time and boolean columns
        time_column = df['TIME']
        dio_send_column = df['DIO SEND']
        dao_send_column = df['DAO SEND']

        # Create subplots for DIO SEND and DAO SEND
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 4))  # Adjust figsize to reduce the vertical size

        # Set y-axis limits and ticks
        ax1.set_ylim(0, 1)
        ax1.set_yticks([0, 1])
        ax2.set_ylim(0, 1)
        ax2.set_yticks([0, 1])

        # Customize x-axis ticks and labels
        num_points = len(time_column)
        x_ticks = np.arange(0, num_points, num_points // 5)  # Create ticks at 1-minute intervals
        x_labels = ['1 min', '2 min', '3 min', '4 min', '5 min']  # Custom labels

        ax1.set_xticks(x_ticks)
        ax2.set_xticks(x_ticks)

        # Ensure that the number of labels matches the number of ticks
        if len(x_ticks) == len(x_labels):
            ax1.set_xticklabels(x_labels)
            ax2.set_xticklabels(x_labels)
        else:

            print("Error: The number of labels does not match the number of ticks.")

        ax1.plot(time_column, dio_send_column, label='DIO SEND', marker='o', linestyle='-')
        ax1.set_ylabel('DIO SEND (Binary)')
        ax1.set_title(f'{sheet_name} - DIO SEND')

        ax2.plot(time_column, dao_send_column, label='DAO SEND', marker='o', linestyle='-')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('DAO SEND (Binary)')
        ax2.set_title(f'{sheet_name} - DAO SEND')

        # Adjust layout and display
        plt.tight_layout()
        plt.show()
    else:
        print(f"Sheet '{sheet_name}' does not contain the required columns.")
