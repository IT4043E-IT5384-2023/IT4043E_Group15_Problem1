# Scraping parameters
LIMIT = 20
KEYWORDS = ['bitcoin', 'DeFi', 'crypto', 'blockchain', 'NFT']
N_TWEETS = 3000
BATCH_SIZE = 50

# Data paths
ROOT = "gs://it4043e-it5384/it4043e/it4043e_group15_problem1"
ACCOUNT_DB_PATH = "twitter/scrapers/accounts.db"
UID_PATH = "output/uids.json"
PROFILE_PATH = "output/profiles.json"
FOLLOW_PATH = 'output/follows.json'
LOG_PATH = "output/log.json"
LOCATION_PATH = "output/location.json"
REPORT_PATH = "output/results/reports.json"
GG_LUCKY_PATH = "/opt/bucket_connector/lucky-wall-393304-3fbad5f3943c.json"

PROCESS_DIR = "output/processed"
CLEAN_DIR = "output/cleaned"
MODEL_CKPT = "gs://it4043e-it5384/it4043e/it4043e_group15_problem1/output/models/spark_rf-n_estimators_95-max_depth_11_noscale"

SPARK_MASTER = "spark://34.142.194.212:7077"
HADOOP_CONNECTOR_PATH = "/opt/spark/jars/gcs-connector-latest-hadoop2.jar"
ELASTIC_MASTER = 'http://34.143.255.36:9200/'
ELASTIC_HTTP_AUTH = {"id": 'elastic', "password": 'elastic2023'}

# Knowledge dictionaries
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

LANG_MAP = {
    'ar': 1,
    'art': 0,
    'bn': 2,
    'ca': 3,
    'cs': 4,
    'cy': 5,
    'da': 6,
    'de': 7,
    'el': 8,
    'en': 9,
    'es': 10,
    'et': 11,
    'eu': 12,
    'fa': 13,
    'fi': 14,
    'fr': 15,
    'he': 16,
    'hi': 17,
    'hu': 18,
    'ht': 19,
    'in': 20,
    'it': 21,
    'iw': 22,
    'ja': 23,
    'ko': 24,
    'lt': 25,
    'lv': 26,
    'ml': 27,
    'msa': 28,
    'ne': 29,
    'nl': 30,
    'no': 31,
    'pl': 32,
    'ps': 33,
    'pt': 34,
    'qam': 0,
    'qct': 0,
    'qht': 0,
    'qme': 0,
    'qst': 0,
    'ro': 35,
    'ru': 36,
    'sl': 37,
    'sr': 38,
    'sv': 39,
    'th': 40,
    'tl': 41,
    'tr': 42,
    'uk': 43,
    'und': 0,
    'ur': 44,
    'vi': 45,
    'zh': 46,
    'zxx': 0,
    'unk': 0,
}