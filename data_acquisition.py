import requests
import pandas as pd
import time

#API Keys:
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
BASE_URL = "https://api.themoviedb.org/3"


def fetch_top_rated_movies(pages=100):
    #1. Fetch genre mapping:
    genre_resp = requests.get(f"{BASE_URL}/genre/movie/list",
                            params={"api_key": API_KEY, "language": "en-US"})

    print(genre_resp.raise_for_status())
    # print(genre_resp.json())
    # print("\n")
    genres_json = genre_resp.json().get("genres", [])
    # print(genres_json)

    genre_map = {g['id']: g['name'] for g in genres_json}
    # print("\n")
    # print(genre_map)


    '''
    params={"api_key": API_KEY, "language": "en-US"}) means ?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US
    Instead of sticking ?api_key=...&language=... directly in the URL, we give them as a dictionary (params). Because:

    Cleaner code → easier to read.
    Safer → no need to worry about ? and & placement.
    Easier to change → if you want a different language (fr-FR for French), just change the dictionary.
    '''

    '''
    #genre_resp.raise_for_status()


    genre_resp is the response we got when we asked the TMDb API:
    → “Please give me the list of genres.”

    Every response from a website (API) has a status code:
    200 → Everything is OK ✅
    404 → Not found (like a broken link) ❌
    401 → Unauthorized (wrong API key) 🔑
    500 → Server problem 🖥️💥

    .raise_for_status() is like a safety check:

    If the status code is 200 → do nothing (continue).
    If it’s something else (like 404, 401, 500) → immediately stop the program and show an error.

    👉 Why?
    So we don’t keep working with bad or empty data.
    '''


    '''
    #genres_json = genre_resp.json().get("genres", [])

    genre_resp.json() gives 
    {
    "genres": [
        {"id": 28, "name": "Action"},
        {"id": 35, "name": "Comedy"},
        {"id": 18, "name": "Drama"}
    ]
    }


    .get("genres", []) means look for the key "genres" in the dictionary.

    If it exists → give me its value (the list of genres).
    If it doesn’t exist (maybe API failed) → give me an empty list [] instead, so my program doesn’t crash.

    So now, genres_json looks like:
    [
    {"id": 28, "name": "Action"},
    {"id": 35, "name": "Comedy"},
    {"id": 18, "name": "Drama"}
    ]


    '''

    #2 Prepare lists to build DataFrame
    titles = []
    overviews = []
    genre_names = []

    #3. Iterate through top-rated pages 1 to 471
    for page in range(1, pages+1):
        resp = requests.get(f"{BASE_URL}/movie/top_rated",
                            params={"api_key": API_KEY, "language": "en-US", "page":page})
        
        # print(resp)
        # print(resp.status_code)
        
        if resp.status_code!=200:
            print(f"Warning: got status {resp.status_code} on page {page}, skipping.")
            continue

        data = resp.json()
        # print("\n")
        # print(data)
        # print("\n")
        # print(data.get("results",[]))          # "results":[{"adult":false,"backdrop_path":"/pNjh59JSxChQktamG3LMp9ZoQzp.jpg","genre_ids":[18,80],"id":278, ....]
        for movie in data.get("results",[]):    #movie = [{"adult":false,"backdrop_path":"/pNjh59JSxChQktamG3LMp9ZoQzp.jpg","genre_ids":[18,80],"id":278, ....]
            titles.append(movie.get("title",""))     #[{.....,"title":"The Shawshank Redemption",....}]
            overviews.append(movie.get("overview", ""))    #[{.....,"overview":"Batman raises the stakes in his war on crime. With the help of Lt. Jim Gordon and District Attorney Harvey Dent, Batman sets out to dismantle the remaining criminal organizations that plague the streets. The partnership proves to be effective, but they soon find themselves prey to a reign of chaos unleashed by a rising criminal mastermind known to the terrified citizens of Gotham as the Joker.",....}]


            # Convert genre_ids to names
            ids = movie.get("genre_ids", [])         #[{....,"genre_ids":[18,80],....}]
            # print("\n")
            # print(ids)
            names = [genre_map.get(i, f"Unknown({i})") for i in ids]
            genre_names.append(", ".join(names))

        # Be considerate to API rate limits
        time.sleep(0.5)   #Wait 0.25 seconds before asking for the next page → so we don’t overload the API. 

    #4. Build the DataFrame
    df = pd.DataFrame({
        "movie_name":titles,
        "description": overviews,
        "genre": genre_names
    }) 

    return df       


