import os
from dotenv import load_dotenv
load_dotenv()

import tweepy
import pandas as pd
pd.set_option('display.max_columns', None)

from utils import TWEET_FIELDS, EXPANSIONS, FINAL_FILE_PATH, FINAL_COLUMNS, REPLIES_FILE_PATH, REPLIER_FILE_PATH, COLUMNS, USER_FIELDS
from get_tweets_data import get_df_from_tweets, get_user_df_from_tweets

client = tweepy.Client(
    bearer_token=os.environ['BEARER_TOKEN'],wait_on_rate_limit=True
)



def get_replies(id):
    response = client.search_recent_tweets(
        f'conversation_id:{id}', 
        tweet_fields=TWEET_FIELDS, 
        expansions=EXPANSIONS, 
        max_results=20
    )
    return response

def get_previous_replies_df():
    if os.path.exists(REPLIES_FILE_PATH):
        return pd.read_csv(REPLIES_FILE_PATH)
    return ''

def get_previous_replier_df():
    if os.path.exists(REPLIER_FILE_PATH):
        return pd.read_csv(REPLIER_FILE_PATH)
    return ''


if __name__ == "__main__":
    tweets_data = pd.read_csv(FINAL_FILE_PATH)
    tweets_has_reply_df = tweets_data[tweets_data['reply_count']>=1]

    tweets_df = get_previous_replies_df()
    user_df = get_previous_replier_df()

    for id in tweets_has_reply_df['tweet_id']:
        response = get_replies(id=id)
        print(id,response)
        if not response.data:
            continue
        new_tweets_df = get_df_from_tweets(tweets=response.data, key_term=id)
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

    tweets_df.to_csv(REPLIES_FILE_PATH, index=False)
    user_df.to_csv(REPLIER_FILE_PATH, index=False)