import os
import requests
import pymongo
from dotenv import load_dotenv
from datetime import datetime
from bs4 import BeautifulSoup
import json
import bs4
load_dotenv()

# Connect MongoDB
client = pymongo.MongoClient("mongodb://localhost:27018")
print("DB connected")
db = client["scraping"]
collection = db["special_offers"]

def get_game_offer_finish_date(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        flag = soup.find('p', class_='game_purchase_discount_countdown')
        return flag.get_text() if flag is not None else 'Date not found'

def get_request_from_steam() -> dict[str,any]:
    url = f"https://store.steampowered.com/search/?specials=1"
    
    games_dict = { }

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    games_containers = soup.find(id='search_resultsRows')
    games = games_containers.find_all('a')

    for game in games:
        game_offer_finish_date = get_game_offer_finish_date(game['href'])
    
        game_dict = {
            'game_url' : game['href'],
            'game_name' : game.find(class_='title').get_text(),
            'game_img' : game.find('img')['src'].replace('capsule_sm_120', 'capsule_616x353'), 
            'game_release_date' : game.find(class_='search_released').get_text().strip() or 'No date',
            'game_original_price' : game.find(class_='discount_original_price').get_text(),
            'game_final_price' : game.find(class_='discount_final_price').get_text(),
            'game_discount_percent' : game.find(class_='discount_pct').get_text(),
            'game_offer_finish_date': game_offer_finish_date
        }

        game_name = game.find(class_='title').get_text()
        games_dict[game_name] = game_dict

        
    return games_dict

def save_as_json(body, file_name):    
    today = datetime.today()
    formatted_date = today.strftime("%d %B %Y")
    with open(file_name, 'a') as file:
        file.write("\n")
        json.dump({f"Offers Games from { formatted_date }": body}, file, indent=4)


def save_request_in_db(response_data : dict[str,any]) -> str:
    collection.insert_one(response_data)
    print("Data save in DB successfully.")

def main():

    response = get_request_from_steam()
    save_as_json(response, 'offers_games.json')


if __name__ == "__main__":
    main()

