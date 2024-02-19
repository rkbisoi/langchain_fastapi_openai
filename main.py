import asyncio
from typing import AsyncIterable
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain_openai import ChatOpenAI
import os
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage

from pydantic import BaseModel


load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Message(BaseModel):
    content: str


async def send_message(content: str) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    model = ChatOpenAI(
        openai_api_key=api_key,
        streaming=True, 
        callbacks=[callback]
    )

    task = asyncio.create_task(
        model.agenerate(messages=[[HumanMessage(content=content)]])
    )

    try:
        async for token in callback.aiter():
            yield token
    except Exception as e:
        print(f"Caught Exception: {e}")
    finally:
        callback.done.set()

    await task


@app.post("/stream_chat/")
async def stream_chat(message: Message):
    generator = send_message(message.content)
    return StreamingResponse(generator, media_type="text/event-stream")