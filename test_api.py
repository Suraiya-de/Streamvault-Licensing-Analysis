import os

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TMDB_API_KEY")

response = requests.get(
    "https://api.themoviedb.org/3/movie/551",
    params={"api_key": api_key}
)

print(response.status_code)
print(response.json()["title"])
