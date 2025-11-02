from Mapas.Leitura import read_file_map
from Mapas.GrafoVisibilidade import create_visibility_graph

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
        #deixei comentado o print pq tava ruim, mas ainda nao sei como melhorar
        # print("\n--- Grafo de visibilidade (amostra) ---")
        
        # v_start = generated_map.q_start
        # if v_start in visibility_graph:
        #     print(f"Vizinhos de {v_start}:")
        #     for neighbor, cost in visibility_graph[v_start]:
        #         print(f"{neighbor} ->  (custo: {cost:.2f})")
        # else:
        #     print(f"Ponto inicial {v_start} não tem vizinhos visíveis.")
        
