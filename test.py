from dotenv import load_dotenv
import os
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(openai_api_key=api_key,streaming=True, callbacks=[StreamingStdOutCallbackHandler()],temperature=0)

messages = [
    # SystemMessage(
    #     content="Translate the sentence to Hindi"
    # ),
    HumanMessage(
        content="write a song about sparkling water"
    ),
]

print(chat.invoke(messages))