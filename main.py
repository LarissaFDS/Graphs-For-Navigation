from Mapas.Leitura import read_file_map
from Mapas.GrafoVisibilidade import create_visibility_graph
from Mapas.Plotar import plotar_mapa_completo, plotar_apenas_obstaculos, plotar_comparacao
from Algoritmos.minimum_generator_tree import minimum_generator_tree, print_mgt
from Algoritmos.search_in_tree import search_in_tree, print_path

if __name__ == "__main__":
    archive = "Mapas\\ArquivoMapa.py"
    generated_map = read_file_map(archive)

    if generated_map:
        print("Mapa carregado com sucesso!")
        print(generated_map)
        
        print(f"\n--- Total de vértices: {len(generated_map.all_vertexs)} ---")
        
        print("\n--- Ponto Inicial ---")
        print(generated_map.q_start)
        
        print("\n--- Ponto Final ---")
        print(generated_map.q_goal)
        
        print(f"\n--- Total de Obstáculos: {len(generated_map.obstacles)} ---")
        
        visibility_graph = create_visibility_graph(generated_map)
        mgt = minimum_generator_tree(visibility_graph, generated_map.q_start)
        print_mgt(mgt)
        path_dots = []
        #path_dots.append(generated_map.q_start)
        cost = search_in_tree(mgt, generated_map.q_start, generated_map.q_goal, path_dots)
        print_path(path_dots)
        print(f"Custo total do caminho: {cost:.2f}")
        #deixei comentado o print pq tava ruim, mas ainda nao sei como melhorar
        # print("\n--- Grafo de visibilidade (amostra) ---")
        
        # v_start = generated_map.q_start
        # if v_start in visibility_graph:
        #     print(f"Vizinhos de {v_start}:")
        #     for neighbor, cost in visibility_graph[v_start]:
        #         print(f"{neighbor} ->  (custo: {cost:.2f})")
        # else:
        #     print(f"Ponto inicial {v_start} não tem vizinhos visíveis.")
        
    plotar_apenas_obstaculos(generated_map, salvar=True, nome_arquivo='mapa_obstaculos.png')
    
    plotar_mapa_completo(
        mapa=generated_map,
        grafo=visibility_graph,
        #arvore=,        
        #caminho=,
        salvar=True,
        nome_arquivo='mapa_completo.png'
    )