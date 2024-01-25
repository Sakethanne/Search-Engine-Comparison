import json
import pandas as pd

# Load the results from Google and Bing
with open('google-results.json', 'r') as google_file:
    google_results = json.load(google_file)

with open('results.json', 'r') as bing_file:
    bing_results = json.load(bing_file)

# List to store results for CSV
results_data = []
number_q = 1
# Process each query
for query, google_links in google_results.items():
    if query in bing_results:
        bing_links = bing_results[query]

        # Compute Spearman coefficient (using given ranks)
        google_ranks = {link: rank for rank, link in enumerate(google_links, 1)}
        bing_ranks = {link: rank for rank, link in enumerate(bing_links, 1)}

        # Create a list of common links and their ranks
        common_links = list(set(google_links) & set(bing_links))
        common_ranks_google = [google_ranks[link] for link in common_links]
        common_ranks_bing = [bing_ranks[link] for link in common_links]

        # Check if n is 1
        n = len(common_links)
        if n == 1:
            # Check if the ranks are equal
            if common_ranks_google[0] == common_ranks_bing[0]:
                spearman_coefficient = 1
            else:
                spearman_coefficient = 0
        elif n > 1:
            # Compute differences in ranks (di)
            di = [rank_google - rank_bing for rank_google, rank_bing in zip(common_ranks_google, common_ranks_bing)]
            
            # Compute Spearman coefficient using the given formula
            spearman_coefficient = 1 - (6 * sum([d**2 for d in di])) / (n * (n**2 - 1))
        else:
            spearman_coefficient = 0

        # Append results to the list
        results_data.append({
            'Queries': 'Query '+ str(number_q),
            'Number of Overlapping Results': len(common_links),
            'Percent Overlap': (len(common_links)/10) * 100,
            'Spearman Coefficient': spearman_coefficient
        })

        number_q = number_q + 1

# Create a DataFrame from the results
results_df = pd.DataFrame(results_data)

# Save the DataFrame to a CSV file
results_df.to_csv('query_comparison_results.csv', index=False)

print("Results stored in query_comparison_results.csv")