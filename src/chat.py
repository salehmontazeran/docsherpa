from pathlib import Path

from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.milvus import MilvusVectorStore

from ingestion.load_file_to_documents import load_file_to_documents

documents = load_file_to_documents(Path("../local_data/test.txt"))

vector_store = MilvusVectorStore(
    host="localhost", port="19530", collection_name="docsherpa_vector_store", dim=1536
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
query_engine = index.as_query_engine()
response = query_engine.query("Give me a generic type for table data structure")
print(response)
