import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
import matplotlib.patches as mpatches

def plotar_mapa_completo(mapa, grafo, arvore=None, caminho=None, salvar=False, nome_arquivo='mapa.png'):
    #cores definidas para cada coisinah 
    cor_grafo = 'lightblue'
    cor_arvore = 'green'
    cor_caminho = 'orange'
    cor_padrao = 'black'    
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    #config baisca
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('X', fontsize=12, fontweight='bold')
    ax.set_ylabel('Y', fontsize=12, fontweight='bold')
    ax.set_title('Mapa de navegação com grafo de visibilidade', fontsize=14, fontweight='bold', pad=20)
    
    #desenha obstaculo
    for i, obs in enumerate(mapa.obstacles):                            
        polygon = obs.get_polygon_shapely()
        if polygon and polygon.is_valid:
            coords = list(polygon.exterior.coords)
            
            patch = MplPolygon(coords, facecolor='black', edgecolor='darkred', linewidth=2.5, alpha=0.6,
                             label='Obstáculos' if i == 0 else '')      #cria poligono matplotlib
            ax.add_patch(patch)
    
    #desenha o grafo de visibilidade
    if grafo:                                                           
        edges_plotted = set()                                           #nao desenha a mesma aresta +1x
        for vertex, neighbors in grafo.items():
            for neighbor, cost in neighbors:
                edge = tuple(sorted([vertex.coords, neighbor.coords]))
                
                if edge not in edges_plotted:
                    ax.plot([vertex.x, neighbor.x], [vertex.y, neighbor.y],
                           color=cor_grafo, linewidth=0.5, alpha=0.4, zorder=1)
                    edges_plotted.add(edge)
    
    #desenha arvore
    if arvore:                                                          
        edges_plotted = set()
        for vertex, neighbors in arvore.items():
            for neighbor, cost in neighbors:
                edge = tuple(sorted([vertex.coords, neighbor.coords]))
                
                if edge not in edges_plotted:
                    ax.plot([vertex.x, neighbor.x], [vertex.y, neighbor.y],
                           color=cor_arvore, linewidth=1.5, alpha=0.6, zorder=2,
                           label='Árvore MST' if not edges_plotted else '')
                    edges_plotted.add(edge)
    
    #desenha caminho
    if caminho and len(caminho) > 1:                                    
        caminho_x = [v.x for v in caminho]
        caminho_y = [v.y for v in caminho]
        ax.plot(caminho_x, caminho_y, 
               color=cor_caminho, linewidth=4, marker='o', markersize=8, 
               markerfacecolor='gold', markeredgecolor='darkorange',
               markeredgewidth=2, alpha=0.9, zorder=5, 
               label='Caminho encontrado')
        
        #numera pontos do cmainho 
        for i, v in enumerate(caminho):                                 
            if v != mapa.q_start and v != mapa.q_goal:
                ax.annotate(f'{i}', 
                          xy=(v.x, v.y), xytext=(5, 5), textcoords='offset points',
                          fontsize=8, color='darkorange', fontweight='bold')
    
    #desenha quina dos obstaculos
    for obs in mapa.obstacles:                                          
        for vertex in obs.vertexs:
            ax.plot(vertex.x, vertex.y, 
                   'o', 
                   color='darkred', 
                   markersize=4,
                   zorder=3)
    
    #faz o start
    if mapa.q_start:                                                    
        ax.plot(mapa.q_start.x, mapa.q_start.y, 
               marker='s',  color='red', markersize=15, markeredgecolor='darkred',
               markeredgewidth=2, label='Início', zorder=6)
        
    #faz o goal
    if mapa.q_goal:                                                     
        ax.plot(mapa.q_goal.x, mapa.q_goal.y, 
               marker='*', color='green', markersize=20, markeredgecolor='darkgreen',
               markeredgewidth=2, label='Objetivo', zorder=6) 
   
    bounds = mapa.get_bounds()
    margin = 50
    ax.set_xlim(bounds[0] - margin, bounds[2] + margin)
    ax.set_ylim(bounds[1] - margin, bounds[3] + margin)
    
 
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9, edgecolor='black')
    x_pos = 0.02
    y_pos = 0.98
    y_step = 0.04
    
    bbox_props = dict(boxstyle ='round', facecolor='wheat', alpha=0.8, edgecolor='wheat')

    texto_vertices = f"Vértices: {len(mapa.all_vertexs)}"
    ax.text(x_pos, y_pos, texto_vertices,
            transform=ax.transAxes, fontsize=10, verticalalignment='top', color=cor_padrao, bbox=bbox_props)
    y_pos -= y_step
    
    texto_obstaculos = f"Obstáculos: {len(mapa.obstacles)}"
    ax.text(x_pos, y_pos, texto_obstaculos,
            transform=ax.transAxes, fontsize=10, verticalalignment='top', color=cor_padrao, bbox=bbox_props)
    
    if grafo:
        y_pos -= y_step
        num_edges = sum(len(neighbors) for neighbors in grafo.values()) // 2
        texto_arestas = f"Arestas no grafo: {num_edges}"
        
        ax.text(x_pos, y_pos, texto_arestas,
               transform=ax.transAxes, fontsize=10, verticalalignment='top', color=cor_grafo, fontweight='bold', bbox=bbox_props)
        
    if caminho:
        dist_total = sum(caminho[i].distance(caminho[i+1])               #calcula a dist
                        for i in range(len(caminho)-1))
        texto_caminho = f"Distância do caminho: {dist_total:.2f}"
        
        ax.text(x_pos, y_pos, texto_caminho,
               transform=ax.transAxes, fontsize=10, verticalalignment='top', color=cor_caminho, fontweight='bold',  bbox=bbox_props)
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
        print(f"✓ Imagem salva como '{nome_arquivo}'")
    
    plt.show()


def plotar_apenas_obstaculos(mapa, salvar=False, nome_arquivo='obstaculos.png'):
    fig, ax = plt.subplots(figsize=(10, 8))
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_title('Obstáculos do Mapa', fontsize=14, fontweight='bold')
    
    for i, obs in enumerate(mapa.obstacles):
        polygon = obs.get_polygon_shapely()
        if polygon and polygon.is_valid:
            coords = list(polygon.exterior.coords)
            patch = MplPolygon(coords, 
                             facecolor='lightcoral', edgecolor='darkred', 
                             linewidth=2, alpha=0.7)
            ax.add_patch(patch)
            
            for vertex in obs.vertexs:
                ax.plot(vertex.x, vertex.y, 'ko', markersize=5)
                ax.text(vertex.x + 2, vertex.y + 2, 
                       f'({vertex.x:.1f}, {vertex.y:.1f})', fontsize=8)

    if mapa.q_start:
        ax.plot(mapa.q_start.x, mapa.q_start.y, 
               'gs', markersize=12, label='START')
    if mapa.q_goal:
        ax.plot(mapa.q_goal.x, mapa.q_goal.y, 
               'r*', markersize=15, label='GOAL')
    
    ax.legend()
    bounds = mapa.get_bounds()
    margin = 10
    ax.set_xlim(bounds[0] - margin, bounds[2] + margin)
    ax.set_ylim(bounds[1] - margin, bounds[3] + margin)
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
        print(f"✓ Imagem salva como '{nome_arquivo}'")
    
    plt.show()