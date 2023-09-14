import pandas as pd 
import sys
from get_tweets_data import get_previous_user_df, get_previous_tweets_df
from get_comments import get_previous_replier_df, get_previous_replies_df
from utils import FINAL_COLUMNS, FINAL_FILE_PATH, COMMENTS_FILE_PATH

pd.set_option('display.max_columns', None)
if __name__ == '__main__':
    print(sys.argv)
    if not sys.argv[1]:
        user_df = get_previous_user_df()
        tweets_df = get_previous_tweets_df()
    else:
        user_df = get_previous_replier_df()
        tweets_df = get_previous_replies_df()
    final_df = tweets_df.merge(user_df, left_on='author_id', right_on='id', how='inner')
    final = final_df.rename(columns={'id_x':'tweet_id'},inplace=True)
    final_df.drop_duplicates(subset=['name','username','key_term','text'],inplace=True)
    final_df = final_df.reset_index()
    final_df = final_df[FINAL_COLUMNS]
    if not sys.argv[1]:
        final_df.to_csv(FINAL_FILE_PATH)
    else:
        final_df.to_csv(COMMENTS_FILE_PATH, index=False)