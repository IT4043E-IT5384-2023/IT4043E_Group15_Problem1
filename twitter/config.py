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

MISSING_CN_TO_CNT = {
    "Kosovo": "Europe",
    "Palestinian Territories": "Asia",
    "North Pole": "Arctic",
    "Ascension and Tristan da Cunha": "Africa",
    "Gornja Siga": "Europe"
}

LANG_DICT = {
    'ar': 'Arabic',
    'art': 'emoji only',
    'bn': "Bengali",
    'ca': 'Catalan',
    'cs': 'Czech',
    'cy': 'Welsh',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'es': 'Spanish',
    'et': 'Estonian',
    'eu': 'Basque',
    'fa': 'Farsi',
    'fi': "Finnish",
    'fr': 'French',
    'he': 'Hebrew',
    'hi': "Hindi",
    'hu': 'Hungarian',
    'ht': 'Haitian Creole',
    'in': "Indonesian",
    'it': "Italian",
    'iw': "Hebrew",
    'ja': "Japanese",
    'ko': "Korean",
    'lt':'Lithuanian',
    'lv': 'Latvian',
    'ml': 'Malayalam',
    'msa': 'Malay',
    'ne': 'Nepali',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'pl': 'Polish',
    'ps': 'Pashto',
    'pt': 'Portuguese',
    'qam': 'tweets with mentions only',
    'qct': 'tweets with cashtags only',
    'qht': 'tweets with hashtags only',
    'qme': 'for tweets with media links',
    'qst': 'tweets with a very short text',
    'ro': "Romanian",
    'ru': "Russian",
    'sl': 'Slovenian',
    'sr': 'Serbian',
    'sv': "Swedish",
    'th': 'Thai',
    'tl': 'Not language1',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'und': 'Not language2',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
    'zh': 'Chinese',
    'zxx': 'tweets with either media or Twitter Card only, without any additional text'
}
