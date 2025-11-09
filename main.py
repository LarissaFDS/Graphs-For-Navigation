from Mapas.Leitura import read_file_map, Vertex
from Mapas.GrafoVisibilidade import create_visibility_graph
from Mapas.Plotar import plotar_mapa_completo, plotar_apenas_obstaculos, plotar_comparacao

from Algoritmos.minimum_generator_tree import minimum_generator_tree
from Algoritmos.search_in_tree import search_in_tree, print_path
from Algoritmos.VerticeMaisProximo import ler_posicao_usuario, corrigir_ponto_invalido, vertice_mais_proximo

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def start_menu():
    clear_screen()
    print("─────────────────────────────────────────────────────────")
    print("  Graphs for Navigation in 2D maps")
    print("─────────────────────────────────────────────────────────")
    choice = input("1 - Start\n2 - Info\n3 - Quit\n").strip()
    print("─────────────────────────────────────────────────────────")
    return choice

def info_function():
    msg = """
    ─────────────────────────────────────────────────────────
              Graphs for Navigation in 2D Maps
    ─────────────────────────────────────────────────────────
    Welcome! This program lets you:

      • Load 2D maps from files
      • Build a visibility graph for navigation
      • Compute the Minimum Spanning Tree (MST)
      • Find the optimal path between any START and GOAL
      • Points inside obstacles are automatically corrected
      • Watch the path being built step-by-step in the plots

    For details on how it works, check the README or the code.
    ─────────────────────────────────────────────────────────
    """
    print(msg)
    input("Press Enter to continue...")


def main():
    while True:
        choice = start_menu()
        if choice == '1':
            clear_screen()
            archive = "Mapas\\ArquivoMapa.py"
            generated_map = read_file_map(archive)

            if generated_map:
                print(generated_map)
                
                visibility_graph = create_visibility_graph(generated_map)
                
                mgt = minimum_generator_tree(visibility_graph, generated_map.q_start)
                
                obstacles_polygons = [obs.get_polygon_shapely() for obs in generated_map.obstacles]

                modo = choose_dots_mode()
                
                plot_start_vertex = None
                plot_goal_vertex = None
                
                new_start_vertex = None
                new_goal_vertex = None
                
                final_start_pos = None
                final_goal_pos = None

                if modo == '1':
                    plot_start_vertex = generated_map.q_start
                    plot_goal_vertex = generated_map.q_goal
                    
                    new_start_vertex = generated_map.q_start
                    new_goal_vertex = generated_map.q_goal
                    
                    final_start_pos = generated_map.q_start.coords
                    final_goal_pos = generated_map.q_goal.coords
                    
                else: 
                    pos_start_input = ler_posicao_usuario("\n→ ENTER NEW START POINT (x,y)")
                    pos_goal_input = ler_posicao_usuario("\n→ ENTER NEW GOAL POINT (x,y)")
                
                    plot_start_vertex = Vertex(pos_start_input[0], pos_start_input[1])
                    plot_goal_vertex = Vertex(pos_goal_input[0], pos_goal_input[1])

                    final_start_pos = corrigir_ponto_invalido(pos_start_input, obstacles_polygons)
                    final_goal_pos = corrigir_ponto_invalido(pos_goal_input, obstacles_polygons)

                    try:
                        new_start_vertex = vertice_mais_proximo(final_start_pos, mgt, obstacles_polygons)
                        new_goal_vertex = vertice_mais_proximo(final_goal_pos, mgt, obstacles_polygons)
                        
                    except Exception as e:
                        print(f"\nError: {e}")
                        print("Could not find a path. Try different points.")
                        input("\nPress Enter to return to menu...")
                        continue

                generated_map.q_start = plot_start_vertex
                generated_map.q_goal = plot_goal_vertex

                print(f"\nSTARTING AT: {plot_start_vertex}")
                print(f"ENDING AT: {plot_goal_vertex}")
                
                path_dots = []
                cost = search_in_tree(mgt, new_start_vertex, new_goal_vertex, path_dots)
                
                if cost is not None:
                    final_start_vertex = Vertex(final_start_pos[0], final_start_pos[1])
                    final_goal_vertex = Vertex(final_goal_pos[0], final_goal_pos[1])
                   
                    cost += final_start_vertex.distance(new_start_vertex)
                    cost += final_goal_vertex.distance(new_goal_vertex)
                    
                    path_dots.insert(0, final_start_vertex)
                    path_dots.append(final_goal_vertex)
                    
                    print_path(path_dots)
                    print(f"\nTotal path cost: {cost:.2f}")
                else:
                    print("\nIt was not possible to find a path between the points!")
                
             
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
        
        elif choice == '2':
            info_function()
        elif choice == '3':
            exit()
        else:
            print("Invalid option! Type 1, 2 or 3.")

def choose_dots_mode():
    print("\nChoose your operating mode:")
    print("1 - Use START and GOAL points from file")
    print("2 - Insert new START and GOAL points")

    while True:
        escolha = input("Type your choice (1 or 2): ").strip()
        if escolha in ['1', '2']:
            return escolha
        print("Invalid option! Type 1 or 2.")
        
if __name__ == "__main__":
    main()