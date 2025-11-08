from Mapas.Leitura import read_file_map, Vertex
from Mapas.GrafoVisibilidade import create_visibility_graph
from Mapas.Plotar import plotar_mapa_completo, plotar_apenas_obstaculos, plotar_comparacao

from Algoritmos.minimum_generator_tree import minimum_generator_tree, print_mgt
from Algoritmos.search_in_tree import search_in_tree, print_path
from Algoritmos.VerticeMaisProximo import vertice_mais_proximo, ler_posicao_usuario


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

      • Load 2D maps from files or skip input if you prefer
      • Build a visibility graph for navigation
      • Compute the Minimum Spanning Tree (MST)
      • Find the optimal path between START and GOAL
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
                
                modo = choose_dots_mode()
                
                if modo == '1':
                    start_vertex = generated_map.q_start
                    goal_vertex = generated_map.q_goal
                    
                else:
                    pos_start = ler_posicao_usuario("\n→ START POINT (START)")
                
                    pos_goal = ler_posicao_usuario("\n→ FINAL POINT (GOAL)")
                
                    mgt_temp = minimum_generator_tree(visibility_graph, generated_map.q_start)
                    
                    start_vertex = vertice_mais_proximo(pos_start, mgt_temp)
                    goal_vertex = vertice_mais_proximo(pos_goal, mgt_temp)
                    
                    print(f"\nClosest vertex to START: {start_vertex}")
                    print(f"Closest vertex to GOAL: {goal_vertex}")
                    
                    generated_map.q_start = start_vertex
                    generated_map.q_goal = goal_vertex

                print(f"START: {generated_map.q_start}")
                print(f"GOAL: {generated_map.q_goal}")
                
                mgt = minimum_generator_tree(visibility_graph, generated_map.q_start)
                
                path_dots = []
                cost = search_in_tree(mgt, generated_map.q_start, generated_map.q_goal, path_dots)
                
                if cost is not None:
                    print_path(path_dots)
                    print(f"\nT {cost:.2f}")
                else:
                    print("\nIt was not possible to find a path in between the dots!")
                
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
    print("Choose your operating mode:")
    print("1 - Use START and GOAL points from file")
    print("2 - Insert new START and GOAL points")

    while True:
        escolha = input("Type your choice (1 or 2): ").strip()
        if escolha in ['1', '2']:
            return escolha
        print("Invalid option! Type 1 or 2.")

if __name__ == "__main__":
    main()