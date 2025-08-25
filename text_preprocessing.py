import re
import string
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from autocorrect import Speller
import emoji

# Download required NLTK data (only once)
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

'''
unkt → needed for tokenization (splitting text into words).

stopwords → list of common English words to remove ("is, the, and").

wordnet and omw-1.4 → needed for lemmatization (e.g. “better” → “good”).
'''

print(stopwords.words("english"))        #['a', 'about', 'above', 'after',...]
stop_words = set(stopwords.words("english"))     #stop_words = {'had', 'through', 'but', 'just', "you've",...}
print("\n")
print(stop_words)  

ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()
spell = Speller(lang="en")


# Optional chat/abbreviations dictionary
chat_dict = {
    "u": "you",
    "r": "are",
    "lol": "laughing",
    "omg": "oh my god",
    "idk": "i do not know",
    "btw": "by the way",
    "gr8": "great",
    "b4": "before",
    "l8r": "later",
    # Add more as needed
}


def preprocess_text(text: str) -> str:
    """Clean and preprocess a text string step by step."""

    #1. Lowercasing
    text = text.lower()

    #2. Remove HTML tags
    text = BeautifulSoup(text, 'html.parser').get_text()

    #3. Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+","",text)

    #4. Remove punctuation
    text = text.translate(str.maketrans("","", string.punctuation))   

    '''
    str.maketrans(x, y, z) builds a translation table that tells Python how to replace characters.

    x = characters to replace
    y = characters to replace them with
    z = characters to remove
    '''

    #5. Remove emojis
    text = emoji.replace_emoji(text, replace='')

    #6. tokenize
    tokens = nltk.word_tokenize(text)

    #7. Replace chat/abbreviations
    tokens = [chat_dict.get(word, word) for word in tokens]
    
    '''
    tokens = ["u", "r", "gr8", "movie"] and chat_dict = {"u": "you", "r": "are", "gr8": "great"} => tokens = ['you','are','great','movie']
    chat_dict.get(word, word) => chat_dict.get(key, default)

    1. key → the thing you want to look up in the dictionary.
    2. default → what you want returned if that key doesn’t exist.

    .get(key, default) is a Python dictionary method. It says:
    =>Hey Python, give me dict[key]/corresponding value if the key exists. Otherwise, give me default value. 

    '''

    #8. Spelling Correction
    tokens = [spell(word) for word in tokens]

    #9. remove stopwords
    tokens = [word for word in tokens if word not in stop_words]

    '''
    #tokens = ["this", "is", "a", "movie", "about", "dogs"]
    #stop_words = ("is", "a", "the", "and"...)

    This line says:
    👉 Keep only the words that are not in stop_words.
    '''

    #10. lemmatization
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    #11. Stemming
    tokens = [ps.stem(word) for word in tokens]

    return " ".join(tokens)
    #" ".join(["love", "dog", "play", "park"]) becomes "love dog play park"
