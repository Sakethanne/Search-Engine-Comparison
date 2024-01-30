import json
import random
import time
import requests
import warnings
from bs4 import BeautifulSoup

# Suppress warnings from the 'requests' library
warnings.filterwarnings('ignore')

# Function to generate a random delay
def random_delay():
    delay = random.uniform(0, 1)
    print(f"Waiting for {delay:.2f} seconds.")
    time.sleep(delay)

# Function to scrape results from a Bing search query
def scrape_bing_search_results(query, max_retries=3):
    print(f"Scraping results for query: '{query}'")
    results = set()  # Use a set to store unique links

    for retry in range(max_retries):
        try:
            # Start from the first page and continue until we get 10 unique results
            page = 1
            while len(results) < 10:
                # Bing search URL, incrementing 'first' parameter to access subsequent pages
                search_url = f"http://www.bing.com/search?q={requests.utils.quote(query)}&first={(page - 1) * 10}"

                # Make a request to the Bing search page
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                response = requests.get(search_url, headers=headers)

                # If the request was successful, parse the page
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Find the results using the appropriate selector
                    for result in soup.find_all('li', class_='b_algo'):
                        link = result.find('a')['href']
                        results.add(link)
                        if len(results) >= 10:
                            break  # Break the loop if we have 10 results
                else:
                    print(f"Error retrieving search results for query '{query}' on page {page}. Status code: {response.status_code}")

                # Increment the page number to check the next page of results
                page += 1

                # Add a random delay between requests to avoid being blocked
                random_delay()

                # If we've checked 10 pages and still don't have 10 results, exit the loop
                if page > 10:
                    break

            print(f"Found {len(results)} unique results.")
            return list(results)[:10]  # Return only the top 10 results
        except Exception as e:
            print(f"An error occurred while scraping: {e}")
            print(f"Retrying ({retry + 1}/{max_retries})...")
            time.sleep(2)  # Add a short delay before retrying

    print("Failed to retrieve search results after multiple attempts.")
    return []

# Main function to run the scraping process
def main(file_path):
    print("Starting the scraping process.")
    # Load the queries from the given file
    with open(file_path, 'r') as file: 
        queries = file.read().splitlines()

    search_results = {}
    
    for query in queries:
        query = query.strip()
        results = scrape_bing_search_results(query)
        search_results[query] = results
    
    # Save the results to a JSON file
    with open('bing_results.json', 'w') as outfile:
        json.dump(search_results, outfile, indent=4)

    print("Scraping process completed.")

# Call the main function with the path to the file containing the list of queries
main('queries.txt')
