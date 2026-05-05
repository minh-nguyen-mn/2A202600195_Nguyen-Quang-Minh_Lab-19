def bfs_query(G, entity, hops=2):
    entity = entity.lower()

    if entity not in G:
        return set()

    visited = {entity}
    frontier = {entity}

    for _ in range(hops):
        next_frontier = set()

        for node in frontier:
            neighbors = set(G.neighbors(node))
            next_frontier |= neighbors

        frontier = next_frontier - visited
        visited |= frontier

    return visited


def graph_to_text(G, nodes):
    facts = set()

    for u in nodes:
        for v in G.neighbors(u):
            rel = G[u][v]["relation"]
            facts.add(f"{u} {rel} {v}")

    return "\n".join(facts)