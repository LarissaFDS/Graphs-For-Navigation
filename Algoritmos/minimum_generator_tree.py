""" 
Implementation of Kruskal or Prim algorithm to find the Minimum Generator Tree of a graph.
The goal is to get the Graph, represent it somehow and then apply one of the algorithms.

Important reminder: 
- Each vertex is start and goal + the obstacles vertices. That will be our graph vertices.
- About the edges, it will be the cartesian distance between each pair of vertices.
"""

from Mapas.Leitura import Vertex

def minimum_generator_tree(visibility_graph : dict, start_vertex : Vertex) -> dict:
    """ The use of Prim's algorithm here would be good since the graph is represented as an adjacency list (dictionary)."""
    tree = {}
    visited = set()  # Para marcar os vértices já incluídos na árvore
    visited.add(start_vertex)

    while len(visited) < len(visibility_graph): # Percorre todos os vértices do dicionário, no caso o grafo de visibilidade
        min_edge = None # Aresta de menor custo
        for u in visited:   # Para cada vértice já na árvore
            for v, cost in visibility_graph[u]: # Para cada vizinho do vértice u
                if v not in visited:            # Se o vértice v ainda não foi visitado, ou seja não está na árvore. Isso vai evitar ciclos e garantir a formação de uma árvore.
                    if min_edge is None or cost < min_edge[2]: # Verifica se é a menor aresta até agora
                        min_edge = (u, v, cost)

        if min_edge:
            u, v, cost = min_edge   
            tree.setdefault(u, []).append((v, cost)) # Adiciona a aresta à árvore
            tree.setdefault(v, []).append((u, cost)) # Adiciona a aresta no sentido contrário (árvore não direcionada)
            visited.add(v) # Marca o vizinho como visitado e recomeça o processo, expandindo a árvore. Agora o vizinho que antes não estava na árvore, passa a estar.

    return tree

def print_mgt(tree: dict):
    print("\nÁrvore Geradora Mínima:")
    for vertex, edges in tree.items():
        for neighbor, cost in edges:
            print(f"{vertex} -- {neighbor} (custo: {cost:.2f})")