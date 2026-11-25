import utils.scryfall
import utils.mtgtop8

#TODO change structure to allow for format versatility, eventually expand to modern
def extract_data():
    #Get list of all standard cards with appropriate data
    scryfall_data = utils.scryfall.get_scryfall_data()
    
    #Given URL is for large standard events of the last 2 months, easily exchanged with data for Modern
    #Maybe in the future

    event_data = utils.mtgtop8.scrape_mtgtop8_data("https://www.mtgtop8.com/format?f=ST&meta=46&cp=")
    return scryfall_data, event_data