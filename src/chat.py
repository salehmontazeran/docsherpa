from pathlib import Path

import streamlit as st
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.vector_stores.milvus import MilvusVectorStore

from src.ingestion.load_file import load_file_to_documents


@st.cache_resource(show_spinner=False)
def create_chat_engine() -> BaseChatEngine:
    # TODO: I think every time we ingest our data to the db.
    # We must make sure some sort of duplication avoidance
    documents = load_file_to_documents(Path("local_data/test.txt"))
    vector_store = MilvusVectorStore(
        host="localhost", port="19530", collection_name="docsherpa_vector_store", dim=1536
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    return index.as_chat_engine()
