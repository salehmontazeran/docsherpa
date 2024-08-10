from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

from src.resources import embed_model, gpt4_o

CHROMA_PATH = "chroma_db"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:
{context}
 - -
Answer the question based on the above context: {question}
"""


def chat_engine_v1(query_text: str) -> str:
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embed_model)

    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0:
        print("Unable to find matching results.")
        raise Exception("we can't find anythings.")
    for i, r in enumerate(results):
        print(f"Chnunk {i}")
        print(r[0].page_content)
        print("-----------------")
    print("==============================")

    context_text = "\n\n - -\n\n".join([doc.page_content for doc, _score in results])

    # Create prompt template using context and query text
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    response_text = gpt4_o.invoke(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]

    formatted_response = f"{response_text.content} \n\n\n Sources: {sources}"
    return formatted_response
