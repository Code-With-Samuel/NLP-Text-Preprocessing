from data_acquisition import fetch_top_rated_movies
from text_preprocessing import preprocess_text

# ✅ Call the function
if __name__ == "__main__":
    df = fetch_top_rated_movies(pages=10)   # test with 10 pages first

    df['description']= df['description'].apply(preprocess_text)
    print(df.head(10))
    df.to_csv("top_rated_movies_with_genres.csv", index=False)
    print("✅ Data saved to CSV")

