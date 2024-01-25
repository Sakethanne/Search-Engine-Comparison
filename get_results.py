import requests
from bs4 import BeautifulSoup
import time
import json

def fetch_search_results(query):
    url = f"http://www.bing.com/search?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def extract_results(html):
    results = set()  # Use a set to store unique links
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('a.tilk')
    

    for link in links:  # Extracting all results
        url = link.get('href', '')
        if url:  # Check if the URL is not empty
            results.add(url)
            if len(results) == 10:
                break  # Stop fetching once there are 10 unique results

    return list(results)  # Convert the set to a list before returning


# Open the file in read mode
with open('queries.txt', 'r') as file:
    # Read all lines from the file
    queries = file.readlines()

# Dictionary to store results
results_dict = {}

querynumber = 1
# Process each query
for q in queries:
    query = q.strip()
    
    # Fetch results until there are 10 unique ones
    while True:
        html = fetch_search_results(query)

        if html:
            search_results = extract_results(html)
            if len(search_results) == 10:
                results_dict[query] = search_results
                break
        else:
            print(f"Failed to fetch search results for query: {query}")

    print(querynumber)
    time.sleep(10)
    querynumber = querynumber + 1

# Save results to a JSON file
with open('results.json', 'w') as json_file:
    json.dump(results_dict, json_file, indent=2)

print("Results stored in results.json")
