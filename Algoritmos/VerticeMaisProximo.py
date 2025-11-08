from Mapas.Leitura import Vertex
import math

def vertice_mais_proximo(posicao: tuple, arvore: dict) -> Vertex:
    if not arvore:
        raise ValueError("Empty tree!")
    
    x_pos, y_pos = posicao
    min_distancia = float('inf')
    vertice_proximo = None
    
    #percorre todos os vértices da árvore
    for vertice in arvore.keys():
        distancia = math.sqrt((vertice.x - x_pos)**2 + (vertice.y - y_pos)**2)
        
        if distancia < min_distancia:
            min_distancia = distancia
            vertice_proximo = vertice
    
    return vertice_proximo

def ler_posicao_usuario(mensagem: str) -> tuple:
    print(mensagem)
    while True:
        try:
            entrada = input("Type the coordinates in the format 'x,y' (ex: 25,15): ")
            x, y = map(float, entrada.strip().split(','))
            return (x, y)
        except ValueError:
            print("Invalid format! Use the format 'x,y' with numbers.")

            
            
'''
    ta considerando o start/goal anterior como um vertice, tem que arrumar
    arrume para colisão também
    na plotagem, tente rotacionar, ta ao contrário
'''
            