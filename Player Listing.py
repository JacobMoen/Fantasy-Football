import requests
import pandas as pd
import numpy as np

league_id = '293551'

# Define the API endpoint for fetching player listing
url = f'https://www.fleaflicker.com/api/FetchPlayerListing'

# Set up query parameters
params = {
    'league_id': league_id
}

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON data
    print(data)  # Debug: print the data to understand the JSON structure

    # Extract player listing information
    players = data.get('players', [])

    if players:
        # Normalize the player data to create a DataFrame
        try:
            df = pd.json_normalize(
                players,
                errors='ignore'
            )

            # Save the DataFrame to an Excel file
            df.to_excel('player_listing.xlsx', index=False)
            print("Data saved to player_listing.xlsx")
        except KeyError as e:
            print(f"Key error during normalization: {e}")
    else:
        print("No players found in the response.")
else:
    print(f"Failed to fetch data: {response.status_code}")
