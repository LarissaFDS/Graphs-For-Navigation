from Mapas.Leitura import Vertex
import math
from shapely.geometry import LineString, Point
from shapely.ops import nearest_points

def corrigir_ponto_invalido(posicao: tuple, obstacles_polygons: list):
    user_point = Point(posicao)
    
    for polygon in obstacles_polygons:
        if polygon.contains(user_point):
            _, p_on_exterior = nearest_points(polygon.exterior, user_point)
            new_posicao = (p_on_exterior.x, p_on_exterior.y)
            
            print(f"Point ({posicao[0]:.2f}, {posicao[1]:.2f}) was inside an obstacle.")
            print(f"Automatically moved to: ({new_posicao[0]:.2f}, {new_posicao[1]:.2f})")
            return new_posicao
    return posicao

def ponto_visivel(pos_coords: tuple, vertice: Vertex, obstacles_polygons: list):
    current_line = LineString([pos_coords, vertice.coords])
    
    for polygon in obstacles_polygons:
        if polygon and polygon.intersects(current_line) and not current_line.touches(polygon):
            return False
    return True

def vertice_mais_proximo(posicao: tuple, arvore: dict, obstacles_polygons: list):
    if not arvore:
        raise ValueError("Empty tree!")
    
    min_distancia = float('inf')
    vertice_proximo = None
    
    for vertice in arvore.keys():
        distancia = math.sqrt((vertice.x - posicao[0])**2 + (vertice.y - posicao[1])**2)
        
        if distancia < min_distancia:
            if ponto_visivel(posicao, vertice, obstacles_polygons):
                min_distancia = distancia
                vertice_proximo = vertice
    
    if vertice_proximo is None:
        raise Exception(
            f"No line-of-sight from position ({posicao[0]:.2f}, {posicao[1]:.2f}) to any tree vertex.\n"
            f"The point is 'trapped' in a dead end. Please try a different point."
        )
    
    return vertice_proximo

def ler_posicao_usuario(mensagem: str):
    print(mensagem)
    while True:
        try:
            entrada = input("Type the coordinates in 'x,y' format (ex: 25,15): ")
            x, y = map(float, entrada.strip().split(','))
            return (x, y)
        except ValueError:
            print("Invalid format! Use 'x,y' with numbers.")