import os
from typing import List

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents import Document

from src.resources import embed_model

DATA_PATH = "../../local_data/llamaindex_docs"
CHROMA_PATH = "../../chroma_db"


def load_documents() -> List[Document]:
    loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.md",
        show_progress=True,
    )
    return loader.load()


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
