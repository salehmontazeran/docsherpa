import os
from typing import List

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document
from langchain_core.utils import convert_to_secret_str
from langchain_openai import OpenAIEmbeddings

DATA_PATH = "../../local_data/llamaindex_docs"
CHROMA_PATH = "../../chroma_db"


def load_documents() -> List[Document]:
    loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.md",
        show_progress=True,
    )
    return loader.load()


embed_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=convert_to_secret_str(
        os.environ["OPENAI_API_KEY"],
    ),
)


def save_to_chroma(docs: List[Document]) -> None:
    if os.path.exists(CHROMA_PATH):
        print("Chroma path already exist!")
        return

    Chroma.from_documents(
        docs,
        embed_model,
        persist_directory=CHROMA_PATH,
    )

    print(f"Saved {len(docs)} docs to {CHROMA_PATH}.")


def generate_data_store() -> None:
    documents = load_documents()
    save_to_chroma(documents)


if __name__ == "__main__":
    generate_data_store()
    generate_data_store()
