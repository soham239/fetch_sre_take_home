"""
HTTP Endpoint Availability Monitor
Performs timely health checks on a list of endpoints and maintains overall status
of the health checks for all domains in the list
"""
import argparse
import sys
import time
import signal
import yaml
import requests

# Global variables to store results
domain_results = {}

def read_config_file(file_path):
    """
    Read input config file in YAML format using PyYAML library
    """
    with open(file_path, 'r', encoding='utf8') as file:
        data = yaml.safe_load(file)
    return data

def send_http_request(endpoint):
    """
    Method to call http endpoint and check for status
    If response code is not 2xx or if latency is more than 500ms
    Server is considered to be DOWN, else UP
    """
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)

    try:
        start_time = time.time()
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=60)
        elif method == 'POST':
            if body is not None:
                response = requests.post(url, headers=headers, data=body, timeout=60)
            else:
                response = requests.post(url, headers=headers, timeout=60)
        else:
            print(f"Unsupported HTTP method: {method}")
            return False
        end_time = time.time()
        response_latency = (end_time - start_time) * 1000  # Convert to milliseconds
        return 300 > response.status_code >= 200 and response_latency <= 500
    except requests.exceptions.RequestException:
        return False

def calculate_availability():
    """
    Method to calculate cumulative domain availability and print to console
    """
    for domain_name, results in domain_results.items():
        # domain_results stores [UP, TOTAL]
        availability_percentage = (results[0] / results[1]) * 100
        print(f"{domain_name} has {int(round(availability_percentage))}% availability percentage")

def signal_handler(sig, frame):
    """
    Method to handle Ctrl+C termination gracefully
    """
    print(f"{sig} {frame}")
    print("\nReceived Ctrl+C. Exiting gracefully...")
    sys.exit()

def main(config):
    """
    Main function to keep checking health status of websites every 15 secs
    """
    while True:
        for http_endpoint in config:
            result = send_http_request(http_endpoint)

            # Domain is extracted from http_endpoint since
            # endpoint --> https://<domain>/<rest_of_url>
            domain = http_endpoint['url'].split('//')[1].split('/')[0]

            # domain_results stores [UP, TOTAL]
            if domain not in domain_results:
                domain_results[domain] = [0,0]

            if result:
                # Mark UP requests as 1
                domain_results[domain][0] += 1
                domain_results[domain][1] += 1
            else:
                # Mark DOWN requests as 0
                domain_results[domain][0] += 0
                domain_results[domain][1] += 1

        # Calculate cumulative availablity and print out result
        calculate_availability()

        # Sleep for 15 secs before doing next health check
        time.sleep(3)

if __name__ == "__main__":
    # Read config file path from command line and call main function
    parser = argparse.ArgumentParser(description="HTTP Endpoint Availability Monitor")
    parser.add_argument("config_file", type=str, help="Path to the YAML configuration file")
    args = parser.parse_args()

    config_data = read_config_file(args.config_file)

    # Set up signal handler to handle Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    main(config_data)
