from transformers import AutoTokenizer, AutoModel
import preprocessor as p
import json
import torch

from ..config import *

tokenizer = AutoTokenizer.from_pretrained('Twitter/twhin-bert-base')
model = AutoModel.from_pretrained('Twitter/twhin-bert-base')

def encode_tweet(rawContent, model, tokenizer):
    cleaned_text =  p.clean(rawContent)
    inputs = tokenizer(cleaned_text, max_length = 512, truncation=True, padding=True, return_tensors="pt")
    try:
        with torch.no_grad():
            outputs = model(**inputs)
    except:
        #print(rawContent)
        #print(cleaned_text)
        #print('Next')
        return None
    return outputs['last_hidden_state'][0][0].tolist()

def encode_tweets():
    with open(PROCESSED_PROFILE_PATH,'r') as f:
        user_data = json.load(f)
    keys = list(user_data.keys())
    
    no_user = len(user_data['id'].keys())
    processed_data = {}
    for key in keys:
        if key not in ['rawDescription', 'tweet']:
            processed_data[key] = user_data[key]
    processed_data['descriptionVec'] = {}
    for i in range(no_user):
        processed_data['descriptionVec'][str(i)] = encode_tweet(str(user_data['rawDescription'][str(i)]), model, tokenizer)
    processed_data['tweet'] = {}
    for i in range(no_user):
        processed_data['tweet'][str(i)] = []
        for tweet in user_data['tweet'][str(i)]:
            new_tweet = {}
            for tweet_key in ['date','replyCount','retweetCount','likeCount' ,'quoteCount', 'viewCount']:
                new_tweet[tweet_key] = tweet[tweet_key]
            if tweet['place'] is None:
                new_tweet['country'] = None
                new_tweet['countryCode'] = None
            else:
                new_tweet['country'] = tweet['place']['country']
                new_tweet['countryCode'] = tweet['place']['countryCode']
            new_tweet['lang'] = LANG_DICT[tweet['lang']]
            new_tweet['textVec'] = encode_tweet(str(tweet['rawContent']), model, tokenizer)
            processed_data['tweet'][str(i)].append(new_tweet)

    with open(PROCESSED_ALL_PATH, 'w') as f:
        json.dump(processed_data, f, indent=4)