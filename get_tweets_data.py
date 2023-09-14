import os
from dotenv import load_dotenv
import tweepy
import pandas as pd

_ = load_dotenv()

from utils import COLUMNS, KEY_TERMS, flatten_dict, EXPANSIONS, TWEET_FIELDS, TWEET_FILE_PATH, USER_FILE_PATH, USER_FIELDS


client = tweepy.Client(
    bearer_token=os.environ['BEARER_TOKEN'],wait_on_rate_limit=True
)

def get_previous_tweets_df():
    if os.path.exists(TWEET_FILE_PATH):
        return pd.read_csv(TWEET_FILE_PATH)
    return ''

def get_previous_user_df():
    if os.path.exists(USER_FILE_PATH):
        return pd.read_csv(USER_FILE_PATH)
    return ''

def get_df_from_tweets(tweets, key_term):
    data_dict = {}
    for record in tweets:
        data = flatten_dict(record.data)
        for column in COLUMNS:
            if column in data_dict:
                data_dict[column].append(data.get(column) if column!='key_term' else key_term)
            else: 
                data_dict[column]=[ data.get(column) if column!='key_term' else key_term]

    return pd.DataFrame(data_dict)

def get_user_df_from_tweets(users):
    user_dict = {}
    for user in users:
        for field in USER_FIELDS:
            if field in user_dict:
                user_dict[field].append(user[field])
            else:
                user_dict[field] = [user[field]]

    return pd.DataFrame(user_dict)


def get_tweets(term):
    response = client.search_recent_tweets(
        f'"{term}" ', 
        tweet_fields=TWEET_FIELDS, 
        expansions=EXPANSIONS, 
        max_results=100
    )
    return response


if __name__ == '__main__':

    tweets_df = get_previous_tweets_df()
    user_df = get_previous_user_df()

    for term in KEY_TERMS:
        response = get_tweets(term=term)
        new_tweets_df = get_df_from_tweets(tweets=response.data, key_term=term)
        new_users_df = get_user_df_from_tweets(response.includes['users'])
        if isinstance(tweets_df, pd.DataFrame)  and isinstance(user_df , pd.DataFrame):
            tweets_df = tweets_df[COLUMNS]
            user_df = user_df[USER_FIELDS]
            
            # tweets_df.drop_duplicates(inplace=True)
            # user_df.drop_duplicates(inplace=True)
            tweets_df = pd.concat([tweets_df, new_tweets_df]).reset_index()
            user_df = pd.concat([user_df, new_users_df]).reset_index()
        else:
            user_df = new_users_df
            tweets_df = new_tweets_df
    
    tweets_df = tweets_df[COLUMNS]
    user_df = user_df[USER_FIELDS]

    tweets_df.to_csv(TWEET_FILE_PATH)
    user_df.to_csv(USER_FILE_PATH)