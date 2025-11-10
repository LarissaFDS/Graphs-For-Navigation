import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
import matplotlib.patches as mpatches

#cores definidas para cada coisinah 
cor_grafo = 'gold'
cor_arvore = "crimson"
cor_caminho = 'green'
cor_obstaculo = 'grey'
cor_padrao = 'black'   
    
def plotar_mapa_completo(mapa, grafo, arvore=None, caminho=None, salvar=False, nome_arquivo='mapa.png'): 
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
            
            patch = MplPolygon(coords, facecolor=cor_obstaculo, edgecolor='black', linewidth=2.5, alpha=0.6,
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
                           color=cor_grafo, linewidth=1.5, alpha=0.4, zorder=1)
                    edges_plotted.add(edge)
    
    #desenha arvore
    if arvore:                                                          
        edges_plotted = set()
        for vertex, neighbors in arvore.items():
            for neighbor, cost in neighbors:
                edge = tuple(sorted([vertex.coords, neighbor.coords]))
                
                if edge not in edges_plotted:
                    ax.plot([vertex.x, neighbor.x], [vertex.y, neighbor.y],
                           color=cor_arvore, linewidth=1.8, alpha=0.6, zorder=6)
                    edges_plotted.add(edge)
    
    #desenha caminho
    if caminho and len(caminho) > 1:                                    
        caminho_x = [v.x for v in caminho]
        caminho_y = [v.y for v in caminho]
        ax.plot(caminho_x, caminho_y, 
               color=cor_caminho, linewidth=4, marker='o', markersize=8, 
               markerfacecolor='green', markeredgewidth=2, alpha=0.9, zorder=5)
        
        #numera pontos do cmainho 
        for i, v in enumerate(caminho):                                 
            if v != mapa.q_start and v != mapa.q_goal:
                ax.annotate(f'{i}', 
                          xy=(v.x, v.y), xytext=(5, 5), textcoords='offset points',
                          fontsize=8, color='darkgreen', fontweight='bold')
    
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
               markeredgewidth=2, label='Início', zorder=6, linestyle='none')
        
    #faz o goal
    if mapa.q_goal:                                                     
        ax.plot(mapa.q_goal.x, mapa.q_goal.y, 
               marker='*', color='green', markersize=20, markeredgecolor='darkgreen',
               markeredgewidth=2, label='Objetivo', zorder=6, linestyle='none') 
   
    bounds = mapa.get_bounds()
    margin = 100
    ax.set_xlim(bounds[0] - margin, bounds[2] + margin)
    ax.set_ylim(bounds[1] - margin, bounds[3] + margin)
    
    ax.invert_yaxis()                                                                                           #arruma o coisa contrario
    
    ax.legend(loc='best', fontsize=10, framealpha=0.9, edgecolor='black')
    x_pos = 0.02
    y_pos = 0.03
    y_step = 0.04
    
    bbox_props = dict(boxstyle ='round', facecolor='white', alpha=0.8, edgecolor='wheat')

    texto_vertices = f"Vértices: {len(mapa.all_vertexs)}"
    ax.text(x_pos, y_pos, texto_vertices,
            transform=ax.transAxes, fontsize=10, verticalalignment='top', color=cor_padrao, bbox=bbox_props)
    y_pos += y_step
    
    texto_obstaculos = f"Obstáculos: {len(mapa.obstacles)}"
    ax.text(x_pos, y_pos, texto_obstaculos,
            transform=ax.transAxes, fontsize=10, verticalalignment='top', color=cor_padrao, bbox=bbox_props)
    
    if grafo:
        y_pos += y_step
        num_edges = sum(len(neighbors) for neighbors in grafo.values()) // 2
        texto_arestas = f"Arestas no grafo: {num_edges}"
        
        ax.text(x_pos, y_pos, texto_arestas,
               transform=ax.transAxes, fontsize=10, verticalalignment='top', color=cor_grafo, fontweight='bold', bbox=bbox_props)
     
    if arvore:
        y_pos += y_step
        num_edges_arvore = sum(len(neighbors) for neighbors in arvore.values()) // 2
        texto_arvore = f"Arestas na MST: {num_edges_arvore}"
        ax.text(x_pos, y_pos, texto_arvore,
               transform=ax.transAxes, fontsize=10, verticalalignment='top', color=cor_arvore, fontweight='bold', bbox=bbox_props)
    
    if caminho:
        y_pos += y_step
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
    ax.set_title('Obstáculos do mapa', fontsize=14, fontweight='bold')
    
    for i, obs in enumerate(mapa.obstacles):
        polygon = obs.get_polygon_shapely()
        if polygon and polygon.is_valid:
            coords = list(polygon.exterior.coords)
            patch = MplPolygon(coords, 
                             facecolor=cor_obstaculo, edgecolor='black', 
                             linewidth=2, alpha=0.7)
            ax.add_patch(patch)
            
            for vertex in obs.vertexs:
                ax.plot(vertex.x, vertex.y, 'ko', markersize=5)
                ax.text(vertex.x + 2, vertex.y + 2, 
                       f'({vertex.x:.0f}, {vertex.y:.0f})', fontsize=8)

    if mapa.q_start:
        ax.plot(mapa.q_start.x, mapa.q_start.y, 
               'rs', markersize=12, label='START')
    if mapa.q_goal:
        ax.plot(mapa.q_goal.x, mapa.q_goal.y, 
               'g*', markersize=15, label='GOAL')
    
    ax.legend()
    bounds = mapa.get_bounds()
    margin = 100
    ax.set_xlim(bounds[0] - margin, bounds[2] + margin)
    ax.set_ylim(bounds[1] - margin, bounds[3] + margin)
    
    ax.invert_yaxis()                                                   #arruma o coisa contrario
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
        print(f"✓ Imagem salva como '{nome_arquivo}'")
    
    plt.show()

#cria uma figura com 4 subplot, so obstaculo, grafo de visibilidade, arvore e caminho final para melhor analise
def plotar_comparacao(mapa, grafo, arvore, caminho, salvar=False, nome_arquivo='comparacao.png'):                    
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    fig.suptitle('Evolução da solução', fontsize=16, fontweight='bold')
    
    def setup_ax(ax, title):                                            #configurar cada subplot
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(title, fontsize=12, fontweight='bold')
        bounds = mapa.get_bounds()
        margin = 100
        ax.set_xlim(bounds[0] - margin, bounds[2] + margin)
        ax.set_ylim(bounds[1] - margin, bounds[3] + margin)
        ax.invert_yaxis()                                               #arruma o coisa contrario
        
    def draw_obstacles(ax):
        for obs in mapa.obstacles:
            polygon = obs.get_polygon_shapely()
            if polygon and polygon.is_valid:
                coords = list(polygon.exterior.coords)
                patch = MplPolygon(coords, facecolor=cor_obstaculo, 
                                 edgecolor='black', linewidth=2, alpha=0.6)
                ax.add_patch(patch)
                
    #apenas obstáculos
    setup_ax(axes[0, 0], '1. Obstáculos')                               
    draw_obstacles(axes[0, 0])
    axes[0, 0].plot(mapa.q_start.x, mapa.q_start.y, 'rs', markersize=12)
    axes[0, 0].plot(mapa.q_goal.x, mapa.q_goal.y, 'g*', markersize=15)
   
    #grafo de visibilidade 
    setup_ax(axes[0, 1], '2. Grafo de visibilidade')                    
    draw_obstacles(axes[0, 1])
    edges_plotted = set()
    for vertex, neighbors in grafo.items():
        for neighbor, cost in neighbors:
            edge = tuple(sorted([vertex.coords, neighbor.coords]))
            if edge not in edges_plotted:
                axes[0, 1].plot([vertex.x, neighbor.x], [vertex.y, neighbor.y],
                              color=cor_grafo, linewidth=0.5, alpha=0.3)
                edges_plotted.add(edge)
    axes[0, 1].plot(mapa.q_start.x, mapa.q_start.y, 'rs', markersize=12)
    axes[0, 1].plot(mapa.q_goal.x, mapa.q_goal.y, 'g*', markersize=15)
    
    #arvore mst
    setup_ax(axes[1, 0], '3. Árvore geradora mínima (MST)')             
    draw_obstacles(axes[1, 0])
    edges_plotted = set()
    for vertex, neighbors in arvore.items():
        for neighbor, cost in neighbors:
            edge = tuple(sorted([vertex.coords, neighbor.coords]))
            if edge not in edges_plotted:
                axes[1, 0].plot([vertex.x, neighbor.x], [vertex.y, neighbor.y],
                              color=cor_arvore, linewidth=2, alpha=0.7)
                edges_plotted.add(edge)
    axes[1, 0].plot(mapa.q_start.x, mapa.q_start.y, 'rs', markersize=12)
    axes[1, 0].plot(mapa.q_goal.x, mapa.q_goal.y, 'g*', markersize=15)
    
    #caminho final
    setup_ax(axes[1, 1], '4. Caminho final')                            
    draw_obstacles(axes[1, 1])
    if caminho and len(caminho) > 1:
        caminho_x = [v.x for v in caminho]
        caminho_y = [v.y for v in caminho]
        axes[1, 1].plot(caminho_x, caminho_y, 'o-', 
                       color=cor_caminho, linewidth=4, 
                       markersize=8, markerfacecolor='green')
    axes[1, 1].plot(mapa.q_start.x, mapa.q_start.y, 'rs', markersize=12)
    axes[1, 1].plot(mapa.q_goal.x, mapa.q_goal.y, 'g*', markersize=15)
    
    plt.tight_layout()
    if salvar:
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
        print(f"✓ Imagem salva como '{nome_arquivo}'")
    plt.show()