import csv
import pandas as pd
import requests

client_id = 'MzU1NDA0ODJ8MTY5OTY0Mzg4OS4zMjA0MDE3'
client_secret = 'c27027be73b80859fb8d7994d7c162b95aab2a7a84417934b4171cbfef82083c'
auth = (client_id, client_secret)
url = 'https://api.seatgeek.com/2/events?datetime_utc.gte=2021-10-07&venue.city=toronto'
params = {'performers.slug': 'toronto-raptors', 'per_page': 50}
response = requests.get(url, auth=auth, params=params)

if response.status_code == 200:
    SCOTIABANK_ARENA_CAPACITY = 19800
    data = response.json().get('events', [])
    formatted_data = {'venue': [], 'home_team': [], 'away_team': [], 
                      'listing_count': [], 'visible_listing_count': [], 'average_price': [], 'lowest_price_good_deals': [], 
                      'lowest_price': [], 'highest_price': [], 'median_price': []}
    for i in range(len(data)):
        formatted_data['venue'].append(data[i]['venue']['name_v2'])
        formatted_data['home_team'].append(data[i]['performers'][0]['name'])
        formatted_data['away_team'].append(data[i]['performers'][1]['name'])
        for stat in data[i]['stats']:
            if stat in formatted_data:
                formatted_data[stat].append(data[i]['stats'][stat])

    df = pd.DataFrame(formatted_data)
    df['attendance'] = df['visible_listing_count'].apply(lambda x: SCOTIABANK_ARENA_CAPACITY - x)
    df.to_csv('raptors-seatgeek-attendance.csv', index=False)