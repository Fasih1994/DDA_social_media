import pandas as pd
import time
from dotenv import load_dotenv
from typing import List
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import SystemMessage, HumanMessage

from tags import Tags
load_dotenv()

prompt_messages = [
    SystemMessage(
        content=(
            "You are a world class algorithm to identify sentiment of tweets"
            "Answers in specific format of sentiment, tone and language"
        )
    ),
    HumanMessagePromptTemplate.from_template("tweet: {tweet}"),
    HumanMessage(
        content="Tips: Make sure to answer in the correct format. Return at least one from field from schema."
    ),
]
chain_prompt = ChatPromptTemplate(messages=prompt_messages)


chain = create_tagging_chain(
    Tags.schema(), 
    ChatOpenAI(temperature=0),
    prompt=chain_prompt
)

def get_sentiment(tweet:str = None):
    result = chain.run(tweet)
    return result['sentiment'], result['tone'], result['language']  



if __name__ == "__main__":
    df = pd.read_csv('data/1st_final.csv')
    df.drop_duplicates(subset=['tweet_id'],inplace=True)
    df= df[['tweet_id', 'name', 'username', 'author_id', 'key_term',
       'text', 'possibly_sensitive', 'lang', 'created_at', 'retweet_count',
       'reply_count', 'like_count', 'quote_count', 'bookmark_count',
       'impression_count', 'conversation_id']]
    dict_sentiment = dict(
        id=[],
        sentiment=[],
        tone=[],
        language=[]
    )

    for i in range(df.shape[0]):
        id = df.iloc[i,0]
        text = df.iloc[i,5]
        dict_sentiment['id'].append(id)
        sentiment,tone,language = get_sentiment(text)
        dict_sentiment['sentiment'].append(sentiment)
        dict_sentiment['tone'].append(tone)
        dict_sentiment['language'].append(language)
        print(sentiment,tone,language)
        time.sleep(1.5)
    sentiment_df = pd.DataFrame(dict_sentiment)
    sentiment_df.to_csv('data/sentiment.csv',index=False)
    final_df = df.merge(sentiment_df, right_on='id', left_on='tweet_id', how='inner')
    final_df = final_df[['tweet_id', 'name', 'username', 'author_id', 'key_term',
        'text', 'possibly_sensitive', 'created_at', 'retweet_count',
        'reply_count', 'like_count', 'quote_count', 'bookmark_count',
        'impression_count', 'conversation_id', 'sentiment','tone', 'language']]
    final_df.to_csv('data/final.csv', index=False)