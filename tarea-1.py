import os
import requests
import pymongo
from dotenv import load_dotenv

load_dotenv()

# Connect MongoDB
client = pymongo.MongoClient("mongodb://localhost:27018")
print("DB connected")
db = client["api_integration"]
collection = db["weather_logs"]

def get_request_from_api(city : str , api_key : str) -> dict[str,any]:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}"
    return requests.get(url).json()


def save_request_in_db(response_data : dict[str,any]) -> str:
    collection.insert_one(response_data)
    print("Data save in DB successfully.")

def main():
    lat = 10.500082992210698
    lon = -66.9226594031646
    coordinates = {"lat": lat, "lon": lon}
    city = "London,uk"
    api_key = os.getenv("API_KEY")
    
    response_data = get_request_from_api( city, api_key)
    print(response_data)
    save_request_in_db(response_data)


if __name__ == "__main__":
    main()
