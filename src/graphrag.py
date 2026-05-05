from src.llm import chat_completion
from src.query_engine import bfs_query, graph_to_text


def extract_entity(question):
    return question.split()[-1].replace("?", "").lower()


def answer_graph(question, G):
    entity = extract_entity(question)

    nodes = bfs_query(G, entity)
    context = graph_to_text(G, nodes)

    prompt = f"""
    Answer using ONLY the context.

    Context:
    {context}

    Question:
    {question}
    """

    return chat_completion(prompt)