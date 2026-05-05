from src.llm import chat_completion


def extract_triples(text):
    prompt = f"""
    Extract knowledge triples.

    STRICT RULES:
    - Format EXACTLY: (Entity, Relation, Entity)
    - One triple per line
    - NO numbering
    - NO explanation

    Text:
    {text}
    """

    raw = chat_completion(prompt)
    return parse_triples(raw)


import re

def parse_triples(raw):
    triples = []

    for line in raw.split("\n"):
        line = line.strip()

        # Remove numbering like "1. ", "2) "
        line = re.sub(r"^\d+[\.\)]\s*", "", line)

        # Extract content inside parentheses
        match = re.search(r"\((.*?)\)", line)
        if not match:
            continue

        content = match.group(1)
        parts = [p.strip() for p in content.split(",")]

        if len(parts) == 3:
            triples.append(tuple(parts))

    return triples