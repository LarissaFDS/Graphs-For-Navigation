import itertools
from shapely.geometry import LineString

from .Leitura import Map, Vertex, Obstacle

def create_visibility_graph(mapa: Map):
    print("\nInitializing visibility graph...")
    
    vertexs = mapa.all_vertexs                                                  #pega todos os vertices do mapa
    obstacles_polygon = [obs.get_polygon_shapely() for obs in mapa.obstacles]   #converte os obstaculos em poligonos do shapely
    graph = {}                                                                  #grafo é lista de adjacencia
    
    for v1, v2 in itertools.combinations(vertexs, 2):                           #itera para todos os pares unicos de vrtices
        current_line = LineString([v1.coords, v2.coords])                       #cria linha
        has_obstacle = False
        
        for polygon in obstacles_polygon:                                       #verifica se a linha passa por dentro de um obstaculo
            if polygon and polygon.intersects(current_line) and not current_line.touches(polygon):
                                                                                #verifica se tem interscção e garante que nao é apenas um toque na borda
                has_obstacle = True
                break
            
        if not has_obstacle:                                                    #se nao tiver obstaculo, adiciona no grafo a aresta
            cost = v1.distance(v2)
            
            if v1 not in graph:
                graph[v1] = []
                
            if v2 not in graph:
                graph[v2] = []
                
            graph[v1].append((v2, cost))
            graph[v2].append((v1, cost))

    print(f"Visibility graph created with {len(graph)} nodes.")
    return graph