import os

def flatten_dict(d ):
    """
    Recursively flatten a nested dictionary.

    Args:
    d (dict): The input dictionary.
    parent_key (str): The key representing the parent in the flattened dictionary.
    sep (str): Separator used to concatenate keys.

    Returns:
    dict: A flattened dictionary.
    """
    items = []
    for key, value in d.items():
        new_key = f"{key}"
        if isinstance(value, dict):
            items.extend(flatten_dict(value).items())
        else:
            items.append((new_key, value))
    return dict(items)

COLUMNS = [
    'id', 'author_id', 'key_term', 'text',
    'possibly_sensitive', 'lang', 'created_at', 
    'retweet_count', 'reply_count', 'like_count', 
    'quote_count', 'bookmark_count', 'impression_count', 
    'conversation_id'
    ]

TWEET_FIELDS = ['author_id','conversation_id','created_at',
                'geo','id','in_reply_to_user_id','lang',
                'possibly_sensitive','public_metrics','referenced_tweets',
                'source','text']

USER_FIELDS = ['id', 'name', 'username']

FINAL_COLUMNS = [
    'tweet_id', 'name', 'username', 'author_id', 
    'key_term', 'text', 'possibly_sensitive', 
    'lang', 'created_at', 'retweet_count', 'reply_count', 
    'like_count', 'quote_count', 'bookmark_count',
    'impression_count', 'conversation_id']

KEY_TERMS = '#DigitalDubai, Digital Dubai, #دبي_الرقمية, #DubaiNow, دبي الرقمية'.split(', ')

TWEET_FILE_PATH = os.path.join(os.getcwd(),'data','tweet.csv')
USER_FILE_PATH = os.path.join(os.getcwd(),'data','user.csv')
REPLIES_FILE_PATH = os.path.join(os.getcwd(),'data','replies.csv')
REPLIER_FILE_PATH = os.path.join(os.getcwd(),'data','replier.csv')
FINAL_FILE_PATH = os.path.join(os.getcwd(),'data','1st_final.csv')
COMMENTS_FILE_PATH = os.path.join(os.getcwd(),'data','comments.csv')
EXPANSIONS=['author_id']

