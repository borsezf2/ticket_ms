import requests
import concurrent.futures
import random
import time
from collections import defaultdict

# Define the endpoints
endpoints = [
    "http://10.5.16.212:9050/register",
    "http://10.5.16.212:9050/login",
    "http://10.5.16.212:9050/login_2",
    "http://10.5.16.212:9050/search_train",
    "http://10.5.16.212:9050/book_train",
    "http://10.5.16.212:9050/search_ticket",
    "http://10.5.16.212:9050/ticket_pdf",
    "http://10.5.16.212:9050/cancel_ticket",
    "http://10.5.16.212:9050/add_train",
    "http://10.5.16.212:9050/update_train",
    "http://10.5.16.212:9050/add_ads"
]

# Global dictionaries to store stats
request_counts = defaultdict(int)
latency_stats = defaultdict(list)

# Function to send a GET request to a random endpoint
def send_request():
    endpoint = random.choice(endpoints)
    request_counts[endpoint] += 1
    start_time = time.time()
    try:
        response = requests.get(endpoint)
        latency = time.time() - start_time
        latency_stats[endpoint].append(latency)
        return response.status_code
    except requests.exceptions.RequestException as e:
        latency = time.time() - start_time
        latency_stats[endpoint].append(latency)
        return str(e)

# Main function to run the load test
def main():
    num_requests = 10000  # Total number of requests
    max_workers = 100  # Number of concurrent workers

    c = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_request) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            try:
                c+=1
                print("req id = ",c," : ",future.result())
            except Exception as e:
                print(f"Request generated an exception: {e}")

    # Print stats
    total_requests = sum(request_counts.values())
    print(f"\nTotal requests: {total_requests}")

    for endpoint, count in request_counts.items():
        avg_latency = sum(latency_stats[endpoint]) / len(latency_stats[endpoint])
        print(f"\nEndpoint: {endpoint}")
        print(f"Requests sent: {count}")
        print(f"Average latency: {avg_latency:.4f} seconds")
        print(f"Minimum latency: {min(latency_stats[endpoint]):.4f} seconds")
        print(f"Maximum latency: {max(latency_stats[endpoint]):.4f} seconds")

if __name__ == "__main__":
    main()
