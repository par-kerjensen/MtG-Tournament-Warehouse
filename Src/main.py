from extract import extract_data
#from transform import ()
import pandas as pd


#TODO Transform tables and data into proper form to be loaded into PostGres database.
def main():

    scryfall_df, event_df = extract_data()

    print('done!')
    #transform()

    #load()

def transform(card_df):
    enriched_cards = transform.enrich_data(card_df)

#do transformations here, potentially with more data sources (though I'm not sure what would be best, this seems pretty comprehensive)

#def load():

#At the endpoint of this, post warehouse creation, i want to use BI tools to represent these metagame changes

#This is gonna be cool as hell!  can't wait to get this working and show Tristan and Dal.

if __name__ =="__main__":
    main()