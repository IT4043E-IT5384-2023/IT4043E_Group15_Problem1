import json
from .config import *

def post_process():
    with open(PROFILE_PATH, 'r') as f:
        profiles = json.load(f)
        
    cleaned = {}
    follow = {}
    tweet_keys = profiles[list(profiles.keys())[0]]['tweet'][0].keys()
    for user_id in profiles.keys():
        cleaned[user_id] = {}

        cleaned[user_id]['user'] = profiles[user_id]['user']

        cleaned[user_id]['follower'] = []
        for i in range(len(profiles[user_id]['follower'])):
            cleaned[user_id]['follower'].append(profiles[user_id]['follower'][i]['id_str'])
            if profiles[user_id]['follower'][i]['id_str'] not in follow.keys():
                follow[profiles[user_id]['follower'][i]['id_str']] = profiles[user_id]['follower'][i]

        cleaned[user_id]['following'] = []
        for i in range(len(profiles[user_id]['following'])):
            cleaned[user_id]['following'].append(profiles[user_id]['following'][i]['id_str'])
            if profiles[user_id]['following'][i]['id_str'] not in follow.keys():
                follow[profiles[user_id]['following'][i]['id_str']] = profiles[user_id]['following'][i]


        cleaned[user_id]['tweet'] = []
        for i in range(len(profiles[user_id]['tweet'])):
            cleaned[user_id]['tweet'].append({})
            for tweet_key in tweet_keys:
                if tweet_key != "user":
                    cleaned[user_id]['tweet'][i][tweet_key] = profiles[user_id]['tweet'][i][tweet_key]
                    
    with open(PROFILE_PATH, 'w') as f:
        json.dump(cleaned, f, indent=4, default=str)

    with open(FOLLOW_PATH, 'w') as f:
        json.dump(follow, f, indent=4, default=str)