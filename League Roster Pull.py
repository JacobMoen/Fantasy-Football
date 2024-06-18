import requests
import pandas as pd
import numpy as np

league_id = '293551'

# Define the API endpoint for the league roster
url = f'https://www.fleaflicker.com/api/FetchLeagueRosters?league_id={league_id}'

# Make the API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON data
    print(data)  # Debug: print the data to understand the JSON structure

    # Extract roster information
    rosters = data.get('rosters', [])

    if rosters:
        # Normalize the roster data to create a DataFrame
        try:
            df = pd.json_normalize(
                rosters, 
                'players', 
                ['team', 'team.abbreviation', 'team.id'], 
                record_prefix='player_',
                errors='ignore'
            )
            
            # Fill missing columns with NaN
            if 'team.abbreviation' not in df.columns:
                df['team.abbreviation'] = np.nan
            if 'team.id' not in df.columns:
                df['team.id'] = np.nan
            
            # Save the DataFrame to an Excel file
            df.to_excel('league_roster.xlsx', index=False)
            print("Data saved to league_roster.xlsx")
        except KeyError as e:
            print(f"Key error during normalization: {e}")
    else:
        print("No rosters found in the response.")
else:
    print(f"Failed to fetch data: {response.status_code}")