from Mapas.Leitura import read_file_map, Vertex
from Mapas.GrafoVisibilidade import create_visibility_graph
from Mapas.Plotar import plotar_mapa_completo, plotar_apenas_obstaculos, plotar_comparacao

from Algoritmos.minimum_generator_tree import minimum_generator_tree, print_mgt
from Algoritmos.search_in_tree import search_in_tree, print_path
from Algoritmos.VerticeMaisProximo import vertice_mais_proximo, ler_posicao_usuario

def escolher_modo_pontos():
    print("ESCOLHA O MODO DE OPERAÇÃO")
    print("1 - Usar pontos START e GOAL do arquivo")
    print("2 - Inserir novos pontos START e GOAL")
    
    while True:
        escolha = input("Digite sua escolha (1 ou 2): ").strip()
        if escolha in ['1', '2']:
            return escolha
        print("Opção inválida! Digite 1 ou 2.")

if __name__ == "__main__":
    archive = "Mapas\\ArquivoMapa.py"
    generated_map = read_file_map(archive)

    if generated_map:
        print(generated_map)
        
        visibility_graph = create_visibility_graph(generated_map)
        
        modo = escolher_modo_pontos()
        
        if modo == '1':
            start_vertex = generated_map.q_start
            goal_vertex = generated_map.q_goal
            
        else:
            pos_start = ler_posicao_usuario("\n→ PONTO INICIAL (START)")
          
            pos_goal = ler_posicao_usuario("\n→ PONTO FINAL (GOAL)")
           
            mgt_temp = minimum_generator_tree(visibility_graph, generated_map.q_start)
            
            start_vertex = vertice_mais_proximo(pos_start, mgt_temp)
            goal_vertex = vertice_mais_proximo(pos_goal, mgt_temp)
            
            print(f"\nVértice mais próximo do START: {start_vertex}")
            print(f"Vértice mais próximo do GOAL: {goal_vertex}")
            
            generated_map.q_start = start_vertex
            generated_map.q_goal = goal_vertex

        print(f"START: {generated_map.q_start}")
        print(f"GOAL: {generated_map.q_goal}")
        
        mgt = minimum_generator_tree(visibility_graph, generated_map.q_start)
        #print_mgt(mgt)
        
        path_dots = []
        cost = search_in_tree(mgt, generated_map.q_start, generated_map.q_goal, path_dots)
        
        if cost is not None:
            print_path(path_dots)
            print(f"\nCusto total do caminho: {cost:.2f}")
        else:
            print("\nNão foi possível encontrar um caminho entre os pontos!")
        
        plotar_apenas_obstaculos(
            mapa=generated_map, 
            salvar=True, 
            nome_arquivo='mapa_obstaculos.png'
        )
        
        plotar_mapa_completo(
            mapa=generated_map,
            grafo=visibility_graph,
            arvore=mgt,        
            caminho=path_dots,
            salvar=True,
            nome_arquivo='mapa_completo.png'
        )
        
        plotar_comparacao(
            mapa=generated_map,
            grafo=visibility_graph,
            arvore=mgt,        
            caminho=path_dots,
            salvar=True,
            nome_arquivo='mapa_comparacao.png'
        )