import os

from langchain_core.utils import convert_to_secret_str
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

embed_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=convert_to_secret_str(
        os.environ["OPENAI_API_KEY"],
    ),
)

gpt4_o = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=convert_to_secret_str(
        os.environ["OPENAI_API_KEY"],
    ),
)
