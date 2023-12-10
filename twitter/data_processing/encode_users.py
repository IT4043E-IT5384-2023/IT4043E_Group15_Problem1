import pandas as pd
from tqdm import tqdm
import json
from geopy.geocoders import Nominatim

from ..config import *

def read_country(city):
    """
    Convert cities and returns the country
    """
    geolocator = Nominatim(user_agent="google",timeout=10) #user agent can be any user agent 
    location = geolocator.geocode(city, language="en") #specified the language as some countries are in other lanaguages

    if ('NoneType' in str(type(location))):
        return 'None'
    else:
        country= location.address.split(',')[-1] #split the string based on comma and retruns the last element (country)
        return country.strip()

def encode_users():
    # Create user dataframe
    users = pd.read_json(PROFILE_PATH)
    index = [i for i in range(2150)]
    users = users.transpose()
    users.index=index

    # Extract user information to a dataframe
    user_list = []
    for i in users['user']:
        user_list.append(i)
    user = pd.DataFrame.from_records(user_list,index=index)

    # Drop unnecessary column
    unnecessary = ['profileImageUrl','profileBannerUrl','descriptionLinks','_type','id_str','url','created']
    user.drop(columns=unnecessary, axis=1,inplace=True)

    # Create a list of tweet coresponding to each user, take the first tweet by default, 
    # if there exist unavailable language, take the 2nd,3rd,... tweet until all languages are valid
    tweet_list = []
    for i in users['tweet']:
        if len(i)==0:
            tweet_list.append(tweet_list[len(tweet_list)-1])  
        else:  
            tweet_list.append(i[0])
    tweet = pd.DataFrame.from_records(tweet_list,index=index)

    # A dictionary to convert languages into country
    '''
    lang = tweet['lang'].unique().tolist()
    lst = [
        'United States', 'Spain','Vietnam','France','China','Estonia', 'United States', 'Romania', 'United States', 'United Kingdom',
        'Portugal','Unknown','Turkey', 'Japan', 'United States', 'Afghanistan','Serbia', 'Hungary', 'Italy', 'Philippines', 'Russia',
        'Egypt', 'Germany' ,'United Kingdom', 'United States', 'Korean', 'Indonesia', 'Unknown', 'Thailand', 'India', 'Finland', 'Netherlands', 
        'Poland', 'Greece', 'Nepal', 'Spain'
    ]
    lang_dict = dict(zip(lang,lst))
    lang_dict['uk'] = "Ukraine"
    lang_dict['lt'] = "Lithuanian"
    lang_dict['cs'] = "Czech Republic"
    lang_dict['qct'] = "United States"
    lang_dict['no'] = "Norway"
    lang_dict['ur'] = "Pakistan"
    '''

    with open(LOCATION_PATH) as json_file:
        location_dict = json.load(json_file)

    country =[]
    for i in range(user.shape[0]): 
        if (user['location'][i] == '' or str(user['location'][i]) == 'nan'):
            #country.append(lang_dict[tweet['lang'][i]])
            country.append('None')
        else:
            country.append(location_dict[user['location'][i]].strip())
    user['country'] = country

    '''
    tweet_list = []
    for i in users['tweet']:
        if len(i)<4:
            tweet_list.append(tweet_list[len(tweet_list)-1])  
        else:  
            tweet_list.append(i[3])
    tweet = pd.DataFrame.from_records(tweet_list,index=index)
    '''

    '''
    for i in range(user.shape[0]): 
        if (user['country'][i] == 'Unknown' or user['country'][i] =='None' ):
            user.at[i,'country']=lang_dict[tweet['lang'][i]]
    '''
    
    user['tweet'] = users['tweet']

    #turn all categorical into numerical
    user[['protected','verified','blue','blueType']] = user[['protected','verified','blue','blueType']].fillna(0)
    user[['protected','verified','blue','blueType']] = user[['protected','verified','blue','blueType']].replace([True, 'Business'],1)
    user[['protected','verified','blue','blueType']] = user[['protected','verified','blue','blueType']].replace(False,0)

    user.to_json(PROCESSED_PROFILE_PATH)