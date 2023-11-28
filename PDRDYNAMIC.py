import datetime

def calculate_pdr_and_latency_advanced(file_path):
    # Initialize counters and lists
    sent_request_count = 0
    received_request_count = 0
    sent_response_count = 0
    received_response_count = 0
    total_sent_messages = 0
    total_received_messages = 0
    request_latencies = []
    response_latencies = []

    # Function to convert time string to datetime object
    def get_time(time_str):
        return datetime.datetime.strptime(time_str, '%M:%S.%f')

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Process each line for requests
    for i, line in enumerate(lines):
        parts = line.split('\t')
        time_str, id_str, message = parts[0], parts[1], parts[2]

        # Increment total messages counters
        if 'Sending' in message:
            total_sent_messages += 1
        if 'Received' in message:
            total_received_messages += 1

        # Check for 'Sending request'
        if 'Sending request' in message:
            sent_request_count += 1
            request_num = message.split(' ')[2]

            # Find corresponding 'Received request'
            for j in range(i + 1, len(lines)):
                if f'Received request {request_num}' in lines[j]:
                    received_request_count += 1
                    response_time = get_time(lines[j].split('\t')[0])
                    request_time = get_time(time_str)
                    request_latencies.append((response_time - request_time).total_seconds() * 1000)
                    break

    # Process each line for responses in reverse order
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]
        parts = line.split('\t')
        time_str, id_str, message = parts[0], parts[1], parts[2]

        # Check for 'Received response'
        if 'Received response' in message:
            received_response_count += 1
            response_num = message.split(' ')[2]

            # Find corresponding 'Sending response'
            for j in range(i - 1, -1, -1):
                if f'Sending response' in lines[j] and lines[j - 1].split('\t')[2].split(' ')[2] == response_num:
                    sent_response_count += 1
                    sending_time = get_time(lines[j].split('\t')[0])
                    response_time = get_time(time_str)
                    response_latencies.append((response_time - sending_time).total_seconds() * 1000)
                    break

    # Calculate PDR and average latencies
    pdr_requests = (received_request_count / sent_request_count) * 100 if sent_request_count > 0 else 0
    pdr_responses = (received_response_count / sent_response_count) * 100 if sent_response_count > 0 else 0
    avg_request_latency = sum(request_latencies) / len(request_latencies) if request_latencies else 0
    avg_response_latency = sum(response_latencies) / len(response_latencies) if response_latencies else 0

    return pdr_requests, pdr_responses, avg_request_latency, avg_response_latency, total_sent_messages, total_received_messages

# Path to your file
file_path = 'C:/Users/psaki/Desktop/MAI/650/Project/testingggg2.txt'  # Replace with your file path

# Calculate PDR, latencies, and total messages
pdr_requests, pdr_responses, avg_request_latency, avg_response_latency, total_sent, total_received = calculate_pdr_and_latency_advanced(file_path)
print(f'Packet Delivery Ratio (PDR) for Requests: {pdr_requests}%')
print(f'Packet Delivery Ratio (PDR) for Responses: {pdr_responses}%')
print(f'Average Latency for Requests: {avg_request_latency} milliseconds')
print(f'Average Latency for Responses: {avg_response_latency} milliseconds')
print(f'Total Messages Sent: {total_sent}')
print(f'Total Messages Received: {total_received}')
