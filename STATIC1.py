import matplotlib.pyplot as plt
import pandas as pd
import re
from datetime import datetime

# Reading and parsing the file content
file_path = 'C:/Users/psaki/Desktop/MAI/650/Project/testingggg3.txt'  # Replace with your file path
with open(file_path, 'r') as file:
    content = file.readlines()

# Regular expression to parse the lines
pattern = r'(\d{2}:\d{2}.\d{3})\tID:(\d)\t(.+)'

# Parsing the file for general data
data = []
for line in content:
    match = re.match(pattern, line)
    if match:
        time_str, id_str, action = match.groups()
        time = datetime.strptime(time_str, '%M:%S.%f')
        data.append({'Time': time, 'ID': int(id_str), 'Action': action})

# Creating a DataFrame from the parsed data
df = pd.DataFrame(data)

# Plot for ID=1 based on responses
df_id_1 = df[(df['ID'] == 1) & df['Action'].str.contains('response')]
df_id_1 = df_id_1.groupby('Time').size().cumsum().reset_index(name='Response Count')

# Adjusted part: Adding the transmission time plot for ID=1
id_1_transmission_data = []

for i in range(0, len(content), 4):
    if i+3 < len(content):
        send_response_line = content[i+2].strip()
        receive_response_line = content[i+3].strip()

        send_response_match = re.match(pattern, send_response_line)
        receive_response_match = re.match(pattern, receive_response_line)

        if send_response_match and receive_response_match:
            send_time_str, send_id_str, send_action = send_response_match.groups()
            receive_time_str, receive_id_str, receive_action = receive_response_match.groups()

            if send_id_str == '1' and 'Sending response' in send_action and 'Received response' in receive_action:
                send_time = datetime.strptime(send_time_str, '%M:%S.%f')
                receive_time = datetime.strptime(receive_time_str, '%M:%S.%f')
                time_diff = (receive_time - send_time).total_seconds()
                response_number = int(receive_action.split(' ')[2])

                id_1_transmission_data.append({'Response Number': response_number, 'Time Difference': time_diff})

id_1_transmission_df = pd.DataFrame(id_1_transmission_data)

# Parsing the file for transmission time data for IDs 2-6
transmission_data = []
for i in range(0, len(content), 2):
    send_line = content[i].strip()
    if i+1 < len(content):
        receive_line = content[i+1].strip()

        send_match = re.match(pattern, send_line)
        receive_match = re.match(pattern, receive_line)

        if send_match and receive_match:
            send_time_str, send_id_str, send_action = send_match.groups()
            receive_time_str, receive_id_str, _ = receive_match.groups()

            if send_id_str in ['2', '3', '4', '5', '6'] and 'Sending request' in send_action:
                send_time = datetime.strptime(send_time_str, '%M:%S.%f')
                receive_time = datetime.strptime(receive_time_str, '%M:%S.%f')
                time_diff = (receive_time - send_time).total_seconds()
                message_number = int(send_action.split(' ')[2])

                transmission_data.append({'ID': int(send_id_str), 'Message Number': message_number, 'Time Difference': time_diff})

transmission_df = pd.DataFrame(transmission_data)

# Plotting the transmission time for each ID
fig, axs = plt.subplots(3, 2, figsize=(15, 10))
fig.suptitle('Transmission Time vs. Message Number for IDs 2-6')

for i, id in enumerate(range(2, 7)):
    ax = axs[i // 2, i % 2]
    df_id = transmission_df[transmission_df['ID'] == id]

    ax.plot(df_id['Message Number'], df_id['Time Difference'], marker='o')
    ax.set_title(f'ID: {id}')
    ax.set_xlabel('Message Number')
    ax.set_ylabel('Transmission Time (seconds)')
    ax.grid(True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
