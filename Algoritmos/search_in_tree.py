"Given a tree, we'll implement a function to search for the minimum path between two nodes inside that tree."""
from Mapas.Leitura import Vertex

def search_in_tree(Tree: dict, start_node: Vertex, end_node: Vertex, path_dots, visited=None):
    if visited is None:
        visited = set()

    visited.add(start_node) # Marca o nó atual como visitado, ou seja, evitaremos loop infinito pois já passou por lá
    path_dots.append(start_node) # Adiciona o nó atual ao caminho

    # Condição de parada
    if start_node == end_node:
        return 0

    # Percorre vizinhos
    for neighbor, cost in Tree.get(start_node, []): # Percorre todo o dicionário da árvore
        if neighbor not in visited: # Percorre recursivamente os vizinhos não visitados para encontrar o nó desejado
            sub_path_cost = search_in_tree(Tree, neighbor, end_node, path_dots, visited) # Recursão
            if sub_path_cost is not None:
                return cost + sub_path_cost

    # Se não encontrou caminho a partir daqui, remove o nó do caminho
    # Comentando isso temos todas as passagens do robô
    #path_dots.pop()
    return None



def print_path(path_dots):
    print("\nCaminho encontrado na Árvore Geradora Mínima:")
    for vertex in path_dots:
        print(f"{vertex} -> ", end="")
    print("Fim")