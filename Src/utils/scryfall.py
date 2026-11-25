import pandas as pd
import requests
import io

def get_scryfall_data():

    #Get bulk data object from scryfall
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'MtG Stats ETL Project'
    }
    url = "https://api.scryfall.com/bulk-data/oracle-cards"
    try:
        response = requests.get(url, headers = headers)
    except:
        raise Exception(f'The scryfall request went wrong')

    #Get bulk oracle cards file from scryfall
    bulk_info = response.json()
    bulk_download_uri = bulk_info.get("jsonl_download_uri")
    try:
        response = requests.get(bulk_download_uri, stream = True)
    except:
        raise Exception(f'The scryfall request went wrong')

    #Parse jsonl file into pandas dataframe    
    scryfall_cards = pd.read_json(io.BytesIO(response.content), lines = True, compression = 'gzip')

    #Trim to all cards legal in standard
    legality_frame = pd.json_normalize(scryfall_cards['legalities'])
    standard_cards = scryfall_cards[legality_frame['standard'] == 'legal']

    #Add price columns to each row
    price_frame = pd.json_normalize(standard_cards['prices'])
    standard_cards = pd.merge(standard_cards, price_frame, left_index = True, right_index = True)
    standard_cards['usd'] = pd.to_numeric(standard_cards['usd'], errors = 'coerce')

    #Grab front faces of cards, rename column for image type used, trim to needed fields
    front_face = pd.json_normalize(standard_cards['card_faces'].str[0]).rename(columns = {'image_uris.display' : 'display'})
    front_face = front_face[['name', 'display', 'mana_cost', 'type_line', 'oracle_text', 'power', 'toughness', 'colors']]

    #Several cards do not have front faces because either they are not dual faced in any way, or that information is stored at the top level fields
    #Grab images at the top level for all cards and give them to front display field
    image_frame = pd.json_normalize(standard_cards['image_uris'])['display']
    front_face['display'] = front_face['display'].fillna(image_frame)

    #Fill all null front face information with information grabbed from top level data
    front_face[['name', 'mana_cost', 'type_line', 'oracle_text', 'power', 'toughness', 'colors']] = front_face[['name', 'mana_cost', 'type_line', 'oracle_text', 'power', 'toughness', 'colors']].fillna(standard_cards[['name', 'mana_cost', 'type_line', 'oracle_text', 'power', 'toughness', 'colors']])
    front_face = front_face.add_prefix('front_')

    #Grab alternate faces of cards, no additional work needed
    #If there is an alternate face, its information will be here
    alt_face = pd.json_normalize(standard_cards['card_faces'].str[1]).rename(columns = {'image_uris.display' : 'display'}).add_prefix('alt_')

    #Merge faces into main dataframe
    standard_cards = pd.merge(standard_cards, front_face, left_index = True, right_index = True)
    standard_cards = pd.merge(standard_cards, alt_face, left_index = True, right_index = True)

    #Trim to fields needed for analytics
    standard_cards = standard_cards[['name', 'released_at', 'layout', 'cmc', 'keywords', 'set', 'set_name', 'artist', 'usd', 'front_name', 'front_display', 'front_mana_cost', 'front_type_line', 'front_oracle_text', 'front_power', 'front_toughness', 'front_colors', 'alt_name', 'alt_display', 'alt_mana_cost', 'alt_type_line', 'alt_oracle_text', 'alt_power', 'alt_toughness', 'alt_colors']]

    #Set index to combined name and rename usd to price
    standard_cards = standard_cards.set_index('name').sort_values(by='name').rename(columns = {'usd': 'price'})
    return standard_cards