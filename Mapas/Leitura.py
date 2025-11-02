import math
import re
from shapely.geometry import Polygon                        #pra classe obstacle

class Vertex:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.coords = (self.x, self.y)                      #armazenando como tupla para facilitar o cálculo de distância

    def distance(self, another_vertex):
        return math.dist(self.coords, another_vertex.coords)#o custo da aresta é a distância entre os vértices

    def __repr__(self):
        return f"Vértice({self.x}, {self.y})"               #representação em string

    def __hash__(self):                                     #paara o grafo (chave de dicionario)
        return hash(self.coords)

    def __eq__(self, other):
        return self.coords == other.coords
    
class Obstacle:                                             #armazena uma lista de quinas (vertice) formando o poligono
    def __init__(self):
        self.vertexs = []
        self._polygon = None

    def add_vertex(self, vertex):
        self.vertexs.append(vertex)
        
    def get_polygon_shapely(self):
        if not self._polygon:
            corner_coods = [v.coords for v in self.vertexs]
            
            if len(corner_coods) >= 3:
                self._polygon = Polygon(corner_coods)
                
        return self._polygon

    def __repr__(self):
        return f"Obstáculo(Vértices: {len(self.vertexs)})"  #representação em string

class Map:                                                  #armazena tudo, ponto de inicio e fim, e a lista de Obstaculo
    def __init__(self):
        self.q_start = None
        self.q_goal = None
        self.obstacles = []
        self.all_vertexs = []                               #lista unica com TODOS os vertices. USAR NO GRAFO DE VISIBILIDADE

    def __repr__(self):                                     #representação em string
        return f"Mapa(Start: {self.q_start}, Goal: {self.q_goal}, Obstáculos: {len(self.obstacles)})"

def read_file_map(archive):
    map = Map()
    clean_lines = []
    regex_ignore = re.compile(r"^\s*#.*$|^\s*}?$|^\s*$")
    inside_comment = False
    
    with open(archive, 'r') as graph_map:
        for line in graph_map:
            
            if "'''" in line:                               #tive que ignorar o comentario manualmente pq o regex nao tava fazendo
                inside_comment = not inside_comment
                continue
            
            if inside_comment:
                continue
            
            clean_line = line.split('#')[0].strip()

            if not regex_ignore.match(clean_line):
                clean_lines.append(clean_line)

    try:                                                    #iterador para "consumir" as linhas limpas uma a uma
        iter_line = iter(clean_lines)
        
        x, y = next(iter_line).split(',')
        map.q_start = Vertex(x, y)                          #START
        map.all_vertexs.append(map.q_start)

        x, y = next(iter_line).split(',')
        map.q_goal = Vertex(x, y)                           #GOAL
        map.all_vertexs.append(map.q_goal)

        num_obstacles = int(next(iter_line))                #NUMERO DE OBSTACULOS

        for _ in range(num_obstacles):                      #loop pela quantidade de obstaculos
            obstacle = Obstacle()
            
            num_corner = int(next(iter_line))               #NUMERO DE QUINA DO OBSTACULO
            
            for _ in range(num_corner):                     #loop pelas quinas
                x, y = next(iter_line).split(',')
                v = Vertex(x, y)                            #QUINA
                obstacle.add_vertex(v)
                map.all_vertexs.append(v)
                
            map.obstacles.append(obstacle)
            
    except StopIteration:
        print("Erro: O arquivo de mapa terminou inesperadamente.")
    except Exception as e:
        print(f"Erro ao processar o arquivo de mapa: {e}")
        return None

    return map