import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent

from langchain.agents.agent_toolkits.pandas.base import _get_functions_prompt_and_tools
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.agents import AgentExecutor
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.tools.python.tool import PythonAstREPLTool
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
from langchain.callbacks import get_openai_callback
import pandas as pd

from utils import FINAL_FILE_PATH


load_dotenv('../.flaskenv')
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.max_colwidth',None)



prefix = ("You are a tweet analyst for Digital Dubai Authority."
          "Always return greetings with:"
          """Hi, I am the DDA Social Listening Bot, that can provide you social listening 
insights for these key terms #DigitalDubai, Digital Dubai, #دبي_الرقمية, #DubaiNow and دبي الرقمية. Always list terms in bullet points."""
          "Here are some insights from the data:"
          "- You can use the Pandas DataFrame named 'dda' to analyze tweet's data which is already imported."
          "- Use appropriate filters to focus on specific information."
          "- 'key_term' unique values are :'#DigitalDubai', 'Digital Dubai', '#دبي_الرقمية', '#DubaiNow', 'دبي الرقمية'"
          "- 'sentiment' unique values are :'positive', 'caution', 'negative', 'neutral', 'fear'"
          """-  Columns are: 'tweet_id', 'name', 'username', 'author_id', 'key_term', 'text',
'possibly_sensitive', 'created_at', 'retweet_count', 'reply_count',
'like_count', 'quote_count', 'bookmark_count', 'impression_count',
'conversation_id', 'sentiment', 'tone', 'language'"""    
          "Key Instructions:"
          "- For `Series.str.contains('some_value', regex=True)` Use regex = True first if it gives nan then use regex=False"
          "- Always give aggregated insights against tone, sentiment and language." 
          "- Never truncate commets/tweets/text."
          "- Give detailed answers as much as possible."         
)

system_message = SystemMessage(content=prefix)

MEMORY_KEY = "chat_history" 
prompt = OpenAIFunctionsAgent.create_prompt(
    system_message=system_message,
    extra_prompt_messages=[MessagesPlaceholder(variable_name=MEMORY_KEY)]
)

dda = pd.read_csv(FINAL_FILE_PATH)
def handle_parsing_errors(error):
    msg = """Handel Parsing error yourself!"""
    return msg

def get_agent(chat_history:list = None):
    df_tool = PythonAstREPLTool(
        locals={"dda":dda}, 
        description=("A Python shell. Use this to execute python commands."
                     "Input should be a valid python command. When using this tool, sometimes output is abbreviated"
                     "- make sure it does not look abbreviated before using it in your answer."
                    )
    )

    llm = ChatOpenAI(temperature=0, model=os.environ['MODEL'])

    agent = OpenAIFunctionsAgent(
                llm=llm,
                prompt=prompt,
                tools=[df_tool]
    )

    memory = ConversationBufferWindowMemory(memory_key=MEMORY_KEY, return_messages=True, k=4)
    if len(chat_history)>1:
        for user_message, ai_message in chat_history[:-1]:
            memory.chat_memory.add_user_message(user_message)
            memory.chat_memory.add_ai_message(ai_message)
    # print(memory)
    agent = AgentExecutor(
        agent=agent,
        tools=[df_tool],
        memory=memory,
        max_iterations=7,
        verbose=True,
        handle_parsing_errors=handle_parsing_errors
    )

    return agent


def ask_agent(agent, query):
    """
    Query an agent and return the response as a string.

    Args:
        agent: The agent to query.
        query: The query to ask the agent.

    Returns:
        The response from the agent as a string.
    """

    with get_openai_callback() as cb:
        response = agent.run(query)
        total_tokens = cb.total_tokens
        # prompt_token = cb.prompt_tokens
        # completion_token = cb.completion_tokens
        total_cost = cb.total_cost
        print(f"Tokens {total_tokens} costs {total_cost}")
    # Return the response converted to a string.
    return str(response)