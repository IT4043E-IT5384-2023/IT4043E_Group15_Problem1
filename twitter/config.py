LIMIT = 20
KEYWORDS = ['bitcoin', 'DeFi', 'crypto', 'blockchain', 'NFT']
N_TWEETS = 3000
BATCH_SIZE = 50

ACCOUNT_DB_PATH = "twitter\\scrapers\\accounts.db"
UID_PATH = "output\\uids.json"
PROFILE_PATH = "output\\profiles.json"
FOLLOW_PATH = 'output\\follows.json'
LOG_PATH = "output\\log.json"
LOCATION_PATH = "output\\location.json"

CLEAN_USER_PATH = "output\\cleaned\\users.csv"
CLEAN_TWEET_PATH = "output\\cleaned\\tweets.csv"

PROCESS_USER_PATH = "output\\processed\\users.csv"
PROCESS_TWEET_PATH = "output\\processed\\tweets.csv"
PROCESS_DATA_PATH = "output\\processed\\data.csv"

MODEL_DIR = "output\\models"
RESULT_DIR = "output\\results\\infer.json"

MISSING_CN_TO_CNT = {
    "Kosovo": "Europe",
    "Palestinian Territories": "Asia",
    "North Pole": "Arctic",
    "Ascension and Tristan da Cunha": "Africa",
    "Gornja Siga": "Europe"
}

LABEL_MAP = {
    'Africa': 0, 
    'Antarctica': 1, 
    'Asia': 2, 
    'Europe': 3, 
    'North America': 4,
    'Oceania': 5, 
    'South America': 6,
    'Arctic': 7
}