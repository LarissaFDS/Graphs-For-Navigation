# Practice 2 - Graphs For Navigation

This project was devoloped by Otávio Joshua Costa Brandão Menezes and Larissa Ferreira Dias de Souza for the graph course, aiming to apply graph theory concepts of robot navigation in a 2D enviroment with obstacles.

the solution implemenst a complete pipeline that:
- Reads a map file containing obstacles.
- Builds a Visibility Graph between all vertices (start/goal and obstacles corners).
- Calculates the Minimum Spanning Tree (MST) of this graph using Prim's Algorithm.
- Performs a Recursive Tree Search to find the lowest-cost path between the star and goal points.
- Allows the user to set custom start and goal points, fiding the nearest vertices on the tree.