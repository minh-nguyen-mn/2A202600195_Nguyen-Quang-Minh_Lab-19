import faiss
import numpy as np
from src.llm import chat_completion
from src.embedder import embed


class FlatRAG:
    def __init__(self, docs):
        self.docs = docs
        self.embeddings = np.array(embed(docs), dtype="float32")

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

    def query(self, question, k=2):
        q_emb = np.array(embed([question]), dtype="float32")

        _, idx = self.index.search(q_emb, k)
        context = "\n".join([self.docs[i] for i in idx[0]])

        prompt = f"""
        Context:
        {context}

        Question:
        {question}
        """

        return chat_completion(prompt)