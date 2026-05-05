from src.extractor import extract_triples
from src.graph_builder import build_graph
from src.graphrag import answer_graph
from src.flat_rag import FlatRAG
from src.utils import load_corpus, load_test, save_results
import os

os.makedirs("outputs", exist_ok=True)

# Load
corpus = load_corpus("data/corpus.txt")
test_set = load_test("data/test_set.json")

# Extract triples
triples = extract_triples(corpus)
print("Triples:", triples)

# Build graph
G = build_graph(triples)

# Flat RAG
docs = corpus.split("\n")
flat = FlatRAG(docs)

# Evaluate
results = []

for item in test_set:
    q = item["question"]
    gt = item["ground_truth"]

    flat_ans = flat.query(q)
    graph_ans = answer_graph(q, G)

    results.append({
        "question": q,
        "ground_truth": gt,
        "flat_rag": flat_ans,
        "graph_rag": graph_ans
    })

# Save
save_results(results, "outputs/evaluation.csv")

print("Done. Check outputs/")