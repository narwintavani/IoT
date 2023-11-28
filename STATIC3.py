import matplotlib.pyplot as plt
import pandas as pd
import re
from datetime import datetime

# Reading and parsing the file content
file_path = 'C:/Users/psaki/Desktop/MAI/650/Project/testingggg3.txt'  # Replace with your file path
with open(file_path, 'r') as file:
    content = file.readlines()

# Regular expression to parse the lines
pattern = r'(\d{2}:\d{2}.\d{3})\s*ID:(\d)\s*(.+)'

# Dictionary to store sending times for each response number
send_times = {}

# List to store the calculated response times
response_times = []

for line in content:
    match = re.match(pattern, line)
    if match:
        time_str, id_str, action = match.groups()
        time = datetime.strptime(time_str, '%M:%S.%f')

        if 'Sending response' in action and id_str == '1':
            # Find the corresponding request number in the previous line
            prev_line = content[content.index(line)-1]
            prev_match = re.match(pattern, prev_line)
            if prev_match:
                _, _, prev_action = prev_match.groups()
                response_num = int(prev_action.split()[2])
                send_times[response_num] = time

        elif 'Received response' in action and id_str != '1':
            response_num = int(action.split()[2])
            if response_num in send_times:
                send_time = send_times[response_num]
                receive_time = time
                time_diff = (receive_time - send_time).total_seconds() * 1000  # milliseconds
                response_times.append({'ID': int(id_str), 'Response Number': response_num, 'Time Difference': time_diff})

# Creating a DataFrame from the response times
df = pd.DataFrame(response_times)

# Plotting the response times for each ID (2-6)
fig, axs = plt.subplots(3, 2, figsize=(15, 10))
fig.suptitle('Response Time (ms) vs. Response Number for IDs 2-6')

for i, id in enumerate(range(2, 7)):
    ax = axs[i // 2, i % 2]
    df_id = df[df['ID'] == id]

    ax.plot(df_id['Response Number'], df_id['Time Difference'], marker='o')
    ax.set_title(f'ID: {id}')
    ax.set_xlabel('Response Number')
    ax.set_ylabel('Time Difference (ms)')
    ax.grid(True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
