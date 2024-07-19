import os
from pathlib import Path

import chromadb
import streamlit as st
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from src.ingestion.load_file import load_file_to_documents


@st.cache_resource(show_spinner=False)
def create_chat_engine() -> BaseChatEngine:
    # TODO: I think every time we ingest our data to the db.
    # We must make sure some sort of duplication avoidance
    start_mod = False

    embed_model = OpenAIEmbedding(
        model="text-embedding-3-large", api_key=os.getenv("OPENAI__API_KEY")
    )

    Settings.embed_model = embed_model

    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("quickstart")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection, embed_model=embed_model)

    if start_mod:
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        documents = load_file_to_documents(Path("local_data/test.txt"))
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, embed_model=embed_model
        )
    else:
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model=embed_model,
        )

    return index.as_chat_engine()
