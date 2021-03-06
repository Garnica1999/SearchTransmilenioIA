# -*- coding: utf-8 -*-
"""transmilenio.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ThKYmjGiu9P0Mb2IlOPw6EkG5qLNkvdq

# **Proyecto Transmilenio para buscar la mejor ruta entre multiples estaciones usando algoritmos de busqueda de Inteligencia Artificial**

Hecho por: Carlos Andres Garnica Salazar - 625762
Universidad Catolica de Colombia

Este proyecto consiste en buscar la mejor ruta dentro del sistema de portales y estaciones de transmilenio. Para lograr esto se implementa un sistema de arboles y grafos para hacer busquedas no informadas e informadas con los algoritmos BSF, DFS, UCS y A*


---

Para hacer la representacion sobre un grafo en computacion necesitamos construir varias clases que representen a los nodos, los pesos y la conexion entre ellos.

La principal ventaja es que un arbol es un tipo de grafo, por lo tanto nos serviran las mismas clases para representarlo.

Ademas de las clases se utilizo diccionarios, que es la manera mas facil de representar este tipo de estructuras de datos en Python. Claro, a este tipo de diccionarios van a guardar objetos de instancias de clases (Vertex) con el fin de almacenar multiples valores y datos en un mismo objeto, en vez de hacer multiples diccionarios, accion de programacion que es menos viable.

**Estaciones**

Las estaciones que se implementaron son las siguientes:

> *   Portal Norte
*   Toberin
*   Calle 161
*   Mazuren
*   Calle 146
*   Calle 142
*   Alcala
*   Prado
*   Calle 127
*   Pepe Sierra
*   Calle 106
*   Calle 100
*   La Castellana
*   NQS-Calle 75
*   AV. Chile
*   Simon Bolivar
*   Movistar Arena
*   Campin - U. Antonio Nariño
*   AV. El Dorado
*   CAD
*   Paloquemao
*   Ricaurte
*   San Façon
*   De La Sabana
*   AV. Jiménez
*   Virrey
*   Calle 85
*   Héroes
*   Calle 76
*   Calle 72
*   Flores
*   Calle 63
*   Calle 57
*   Marly
*   Calle 45
*   AV. 39
*   Calle 34
*   Calle 26
*   Calle 22
*   Calle 19
*   Concejo de Bogotá
*   Centro Memoria
*   U. Nacional

Como inicio de la ruta se escogio el Portal norte, mientras que el final de la ruta es la estacion AV. Jimenez.

# **Dependencias**

Este proyecto requiere de ciertas dependencias, las cuales se describen a continuacion:

*   `PriorityQueue`: Clase que permite implementar una cola de prioridad en Python. Para saber mas la documentacion esta [aqui](https://docs.python.org/3/library/queue.html).
*   `Geopy.distance`: Permite implementar metricas de distancia entre 2 puntos terrestes con coordenadas de latitud y longitud. En este caso el algoritmo a utilizar es great_circle. La documentacion de las distancias se encuentra en [este enlace](https://geopy.readthedocs.io/en/stable/#module-geopy.distance).
"""

from queue import PriorityQueue
from geopy.distance import geodesic, great_circle

"""# **Clase Vertex**

> Para poder representar cada nodo del grafo o arbol, necesitamos una clase que englobe esto, ademas que guarde los vecinos o una lista de adyacentes por cada nodo. La siguiente clase se encargara de esto.
"""

class Vertex:
    def __init__(self, node, coordinates):
        self.id = node
        self.coordinates = coordinates # (x,y)
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    '''
    Agrega vecinos dado un objeto de la clase Vertex y su respectivo costo.
    Entrada:
        * neightbor: Obtejo de la clase Vertex que representa un nodo adyacente 
        de este nodo (self).
        * weight: Peso entre el vertice vecino y este nodo (self).
    '''
    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    '''
    Obtiene las conexiones adyacentes en este nodo (self)
    Salida:
        Nodos adyacentes.
    '''
    def get_connections(self):
        return self.adjacent.keys()  

    '''
    Obtiene en forma de lista de enteros los vertices vecinos de este nodo (self)
    Salida:
        Lista con los ids de los nodos adyacentes a este nodo (self).
    '''
    def get_childrens(self):
        return [x.id for x in self.adjacent]

    '''
    Obtiene en forma de lista de la clase Vertes los nodos vecinos de este nodo (self)
    Salida:
        Lista con los objetos de la clase Vertex representando los nodos vecinos de este nodo (self).
    '''
    def get_vertex_childrens(self):
        return [x for x in self.adjacent]

    '''
    Obtener el id de este nodo (self).
    Salida:
        Un entero que representa el id este nodo (self).
    '''
    def get_id(self):
        return self.id

    '''
    Obtiene el peso entre este nodo (self) y un vecino.
    Salida:
        Numero que representa el peso entre este nodo (self) y un vertice vecino.
    '''
    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    '''
    Metodo que obtiene las coordenadas geograficas de un vertice, el cual 
    representa a una estacion del sistema de Transmilenio.
    Salida:
        Coordenadas geograficas en (x,y) de un vertice.
    '''
    def get_coordinates(self):
        return self.coordinates

    '''
    Metodo que construye un diccionario de datos en el formato {id: weight} 
    correspondiente a los nodos adyacentes de este nodo (self).
    Salidas:
        Diccioanrio de datos de los vertices adyacentes de este nodo (self) 
        con sus respectivos pesos.
    '''
    def get_dict_childrens_weights(self):
        dictionary = {}

        for node in self.adjacent:
            node_id = node.get_id()
            node_weight = self.get_weight(node)
            dictionary.setdefault(node_id, node_weight)

        return dictionary

    def __repr__(self):
        return '{}, {}'.format(repr(self.id), repr(self.coordinates))
    
    def __lt__(self,other):
        return (self.id < other.id )
    
    def __gt__(self,other):
        return (self.id  > other.id )

"""# **Clase Grafo**

> Con esta clase se engloba la estructura de datos de un grafo para su correspondiente representacion. Ademas, algunos metodos de esta clase estan diseñados para crear vertices, obtener vertices u obtener el grafo en forma de diccionario de la forma `{int : [list]...}`

Para la construccion del grafo se utilizo diccionarios de la clase vertex.
"""

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    '''
    Permite la iteracion sobre esta clase.
    '''
    def __iter__(self):
        return iter(self.vert_dict.values())

    '''
    Agrega un vertice al diccionario de datos que representa un grafo.
    Entrada:
        * node: ID del nuevo nodo
        * coordinates: Coordenadas de la ubicacion geografica representada 
        logicamente por un vertice.
    Salida:
        Retorna un objeto dela clase Vertex, que representa a el vertice recien
        agregado.
    '''
    def add_vertex(self, node, coordinates):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node, coordinates)
        self.vert_dict[node] = new_vertex
        return new_vertex

    '''
    Obtiene un vertice dado el id de un vertice existente
    Entrada:
        * n: ID de un vertice
    Salida:
        Retorna un objeto de la clase Vertex en caso de encontrar el vertice. 
        En caso contrario devuelve un objeto nulo (None)
    '''
    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None
    '''
    Metodo el cual agrega conexion (arista) dados 2 nodos y un peso.
    Entradas:
        * frm: Coordenadas geograficas del sitio 1
        * to: Coordenadas geograficas del sitio 2
        * cost: El costo entre los 2 vertices
    '''
    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    '''
    Metodo que obtiene todos los vertices del grafo
    Salidas:
        * Lista con todos los vertices del grafo
    '''
    def get_vertices(self):
        return self.vert_dict.keys()

    '''
    Convierte el diccionario {id:obj<Vertex>} en un diccionario {id: list[vecinos...]},
    el cual vecinos representa cada nodo adyacente al nodo id.
    Salida:
        * Diccionario de datos convertido en el formato {id: list[vecinos...]}
    '''
    def get_dictionary(self):
        graph = {}
        for v in self.vert_dict.values():
            graph.setdefault(v.get_id(), v.get_childrens())

        return graph

"""# **Clase Node**

> El uso de esta clase se limita a facilitar la programacion y el manejo de los vertices en el algoritmo A*. Si bien se pudo utilizar la clase Vertex para este objetivo, no es lo mas adecuado, puestoq ue tienen objetivos diferentes, ademas de parametros, algunos similares pero en su mayoria no implmenetados en Vertex por convencion de abstraccion del problema.
"""

class Node:

    # Initialize the class
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.g = 0 # Distancia al nodo de inicio
        self.h = 0 # Distance al nodo objetivo
        self.f = 0 # Total costo

    # Comparacion de los nodos
    def __eq__(self, other):
        return self.name == other.name

    # Ordenamiento de los vertices
    def __lt__(self, other):
         return self.f < other.f

    # Impresion de los nodos
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))

"""# **Clase TreeSearch**

En esta clase se dan todos los metodos de busqueda y recorrido del grafo, incluyendo la busqueda no informada e informada.

> *   BFS `(bfs_shortest_path)`: Busqueda por anchura. Este tipo de busqueda utiliza una cola para guardar los vecinos de un nodo.
*   DFS `(dfs_paths)`: Busqueda por profundidad. Este algoritmo utiliza una pila para almacenar todos los nodos adyacentes de los nodos que ha visitado
*   UCS `(ucs)`: Busqueda por costo unitario. Algoritmo similar a bfs, pero evalua los costos a traves de una cola de prioridades.
*   A* `(astar_search)`: Algoritmod e busqueda informada, el cual tiene en cuenta el costo unitario de un vertice con sus adyacentes, ademas de un costo heristico calculado

Para el calculo heuristico `(construct_heristic)` se midio como la distancia en linea recta desde la estacion AV. Jimenez a las demas estaciones (Distancia total). Esta medicion se hizo utilizando la libreria `Geopy.distance` en la funcion `Station.distance`, usando el algoritmo del gran circulo, el cual toma en cuenta que la tierra es totalmente esferica, con un radio de 6371.008 Km y dando resultados con un error del 0.5% aproximadamente.

Aun asi, se puede utilizar cualquier medicion tomando las coordenadas (longitud y latitud) por cada estacion, como la euclidiana o la distancia de manhattan para dicho proposito. El principal problema es que este tipo de distancias no tienen en cuenta la curvatura del arco, haciendola mas ineficiente para distancias en lugares de la tierra. Para el anterior trabajo esta el metodo `heristic`, el cual, dado 2 coordenadas, devuel ve las mediciones deseadas. Esta funcion se puede usar como complemento para medir todas las distancias, reemplazando a el algoritmo del gran circulo implementado en `GeoPy`.

> Si desea utilizar otro algoritmo de medicion de distancia, consulte la [documentacion de GeoPy para localizaciones](https://geopy.readthedocs.io/en/stable/#module-geopy.distance).
"""

class TreeSearch:

    '''
    Inicializacion
    Entradas:
        *graph: variable la cual puede tomar forma de objeto de la clase Graph
        u objeto de la clase dict, dependiendo del algoritmo a ejecutar debe de 
        cambiarse.
    Excepciones:
        *TypeError: Se produce cuando la variable graph tiene un valor None.
    '''
    def __init__(self, graph):
        if graph is not None:
            self.graph = graph
            self.weights = []
        else:
            raise TypeError('El grafo tiene un valor de instancia incorrecto: None')

    #Algoritmos de busqueda no informada
    '''
    Algoritmo BFS
    Entradas:
        - start: Nodo de entrada de la clase Vertex
        - goal: Nodo objetivo de la clase Vertex
    *Salidas: Lista con la ruta optima encontrada por este algoritmo. Cada indice
    es el id del nodo que pertenece a aquel camino optimo.
    *Excepciones:
        * TypeError: Esta excepcion ocurre cuando el campo de la presente clase graph
        no es la instancia de la clase Graph, sino una matriz o un diccionario.
    '''
    def bfs_shortest_path(self, start, goal):
        if (isinstance(self.graph, dict)):
            raise TypeError('El grafo no es instancia de la clase Graph')

        explored = []

        queue = [[start]]
    
        if start == goal:
            return "El objetivo es el mismo que el inicio."
    
        while queue:
            
            path = queue.pop(0)
            
            node = path[-1]
            if node not in explored:
                neighbours = self.graph.vert_dict[node].get_childrens()
                
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    
                    if neighbour == goal:
                        return new_path
    
                explored.append(node)
    
        return "No hay conexion entre el nodo de inicio y el objetivo."

    '''
    Algoritmo DFS
        - start: id del Nodo de entrada
        - goal: id del Nodo de salida
    Salida: Lista con la ruta optima encontrada por este algoritmo. Cada indice
    es el id del nodo que pertenece a aquel camino optimo.
    Excepciones:
        *TypeError: Se produce cuando el campo graph de la presente clase no 
        es una instacia de la clase dict.
    '''
    def dfs_paths(self, start, goal):
        if(isinstance(self.graph, Graph)):
            raise TypeError('El grafo no es instancia de un diccionario.')

        stack = [(start, [start])]
        while stack:
            (vertex, path) = stack.pop()
            for next in set(self.graph[vertex]) - set(path):
                if next == goal:
                    return path + [next]
                else:
                    stack.append((next, path + [next]))

    '''
    Algoritmo UCS
    Entradas:
        - start: Nodo de entrada de la clase Vertex
        - goal: Nodo objetivo de la clase Vertex
    -Salidas: Lista con la ruta optima encontrada por este algoritmo. Cada indice
    es el id del nodo que pertenece a aquel camino optimo.
    -Excepciones:
        * TypeError: Esta excepcion ocurre cuando el campo de la presente clase graph
        no es la instancia de la clase Graph, sino una matriz o un diccionario.
    '''
    def ucs(self, start, goal):
        if (isinstance(self.graph, dict)):
            raise TypeError('El grafo no es instancia de la clase Graph')

        visited = set()
        queue = PriorityQueue()
        queue.put((0, [start]))

        while queue:
            #cost, node = queue.get()
            pair = queue.get()
            current = pair[1][-1]
            #print(pair[1], type(pair[1]))
            if current not in visited:
                visited.add(current)
                
                
                if current == goal:
                    path = []
                    for u in pair[1]:
                        path.append(u.get_id())
                    return path
                
                for i in self.graph.vert_dict[current.get_id()].get_connections():
                    if i not in visited:
                        total_cost = pair[0] + self.graph.vert_dict[current.get_id()].get_weight(i)
                        new_path = list(pair[1])
                        new_path.append(i)
                        queue.put((total_cost, new_path))
    
    #Algoritmos de busqueda informada
    '''
    Metodo alternativo para la medicion de la heuristica
    Entradas: 
        - graph: objeto de la clase Graph
        - a: Id de un nodo
        - b: id de un nodo
        - method: Indica la metrica de medicion de distancia. Euclidean o 
        manhattan
    Salida: Numero el cual indica la distancia dado 2 puntos o coordenadas de 2
    lugares.
    '''
    def heuristic(self, graph, a, b, method = 'euclidean'):
        #Se obitnene los vertices dado el id del vertice
        node_a = graph.get_vertex(a)
        node_b = graph.get_vertex(b)

        #Se extraen las coordenadas
        (x1, y1) = node_a.get_coordinates()
        (x2, y2) = node_b.get_coordinates()
        if method == 'euclidean':
            return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        elif method == 'manhattan':
            return abs(x1 - x2) + abs(y1 - y2)

    '''
    Algoritmo A* - Dijkstra - Algoritmo Voraz
        * Sera A* cuando exista g(n) y h(n), y estos sean mayores a 0
        * Cuando h(n) = 0 entonces este algoritmo es Dijkstra
        * Cuando g(n) = 0 entonces este algoritmo es un algoritmo voraz
    Entradas:
        - graph: El objeto de la clase Graph
        - heuristics: Diccionario con la distancia total entre un punto de 
        destino y final.
        - start: id del nodo de inicio
        - end: id del vertice el cual es el final del recorrido
        - gn: Booleano el cual indica si activar o no g(n). 
        Si esta desactivado este algoritmo pasa a ser Dijkstra.
    Salida: Lista con la ruta optima encontrada por este algoritmo. Cada indice
    es el id del nodo que pertenece a aquel camino optimo.
    Excepciones:
        * TypeError: Se produce cuando el campo de esta clase graph no es un 
        objeto de la instancia de la clase Graph, o cuando la variable gn es 
        falsa al mismo tiempo que heuristics es None.
    '''

    def astar_search(self, graph, heuristics, start, end, gn = True):
        if (isinstance(self.graph, dict)):
            raise TypeError('El grafo no es instancia de la clase Graph')

        if gn is False and heuristic is None:
            raise TypeError('El parametro gn no puede ser falso al mismo tiempo que heuristics es None')
        # Creacion de las listas para guardar los vertices abiertos y cerrados
        open = []
        closed = []

        # Crear un nodo inicial y final
        start_node = Node(start, None)
        goal_node = Node(end, None)

        # Agregar el nodo de inicio a la lista de vertices abiertos
        open.append(start_node)
        
        # Iterar hasta que la lista de nodos abiertos este vacia
        while len(open) > 0:

            #Ordenar la lista de ndoos abiertos para obtener el vertice con costo mas bajo
            open.sort()

            # Obtner el nodo con el menor costo
            current_node = open.pop(0)

            # Agregar el nodo a la lista de vertices cerrados.
            closed.append(current_node)
            
            # Si se llego al nodo final retornar la ruta mas optima
            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    path.append(str(current_node.name) + ': ' + str(current_node.g))
                    current_node = current_node.parent
                path.append(str(start_node.name) + ': ' + str(start_node.g))
                # Retornar la lista en reversa.
                return path[::-1]

            # Obtener vecinos del nodo actual
            neighbors = graph.get_vertex(current_node.name).get_dict_childrens_weights()

            # Iterar sobre los vecinos del nodo actual
            for key, value in neighbors.items():

                # Crear un nodo vecino
                neighbor = Node(key, current_node)

                # Verificar si el nodo esta en la lista de vertices cerrados
                if(neighbor in closed):
                    continue

                # Calcular el costo de la ruta completa
                neig_node = graph.get_vertex(neighbor.name)
                cost = graph.get_vertex(current_node.name).get_weight(neig_node)

                if gn is True:
                    neighbor.g = current_node.g + cost
                else:
                    neighbor.g = 0

                if heuristics is not None:
                    neighbor.h = heuristics.get(neighbor.name)
                else:
                    neighbor.h = 0
                neighbor.f = neighbor.g + neighbor.h

                #Verificar si el nodo vecino esta en la lista abierta y si este tiene un valor f mas bajo
                if(self.add_to_open(open, neighbor) == True):
                    open.append(neighbor)

        # Retorna None si no se encontro ruta optima
        return None

    '''
    Metodo que verifica si un vecino debe de ser agregado a la lista de vertices
    abiertos. Funcion utilizada para el algoritmo A*

    Entradas:
        * open: Lista de vertices abiertos
        * neighbor: Vertice vecino a evaluar
    Salidas: Retorna verdadero si se cumplen las indicaciones para que el vertice
    vecino sea agregado a la lista de nodos abiertos, de lo contrario retorna 
    falso.
    '''
    # Check if a neighbor should be added to open list
    def add_to_open(self, open, neighbor):
        for node in open:
            if (neighbor == node and neighbor.f > node.f):
                return False
        return True

    '''
    Metodo el cual calcula la funcion heuristica para cada estacion o ubicacion
    geografica.

    Entradas:
        * graph: Grafo de la clase graph
        * station: objeto de la clase Station
    Salida: Diccionario el cual contiene la distancia desde una ubicacion 
    geografica a todas las demas registradas.
    '''
    def construct_heristic(self, graph, station):
        heuristic = {}

        #Obtener el nodo del cual se va a medir la distancia hacia demas
        frm = graph.get_vertex(24)

        #Obtener coordenadas
        coordinates_from = frm.get_coordinates()

        #Iterar en todos los vertices existentes en el grafo
        for i in range(graph.num_vertices):

            #Obtener nodo y coordenadas del nodo a medir su distancia
            to_node = graph.get_vertex(i)
            coordinates_to = to_node.get_coordinates()

            #Calcular la distancia
            dist = station.distance(coordinates_from, coordinates_to)

            #Ingresar estacion y distancia al diccionario
            heuristic.setdefault(i, dist)

        return heuristic

"""# **Clase Station**
Esta clase se encarga de almacenar el diccionario completo de estaciones que se van a utilizar. Para la construccion de este tipo de estructura de datos se utiliza la funcion `build_all_stations`, la cual agrega el nombre de la estacion, y una lista que contiene el id que va a tener dentro de la ejecucion de este proyecto en conjunto con las coordenadas terrestres (latitud, longitud) en la que se ubica la estacion.

> Si bien, este tipo de coordenadas se pueden obtener mediante la libreria `GeoPy` y utilizando algun API de un mapa online como Google maps o Here Maps, requiere realizar la busqueda de la ubicacion exacta para que de como resultado las coordenadas. El problema es que alguna de estas APIs arrojan coordenadas aproximadas o incorrectas de la ubicacion a consultar, sabiendo que la consulta o la busqueda fue correcta.

Es por ello que se ha ingresado todas las coordenadas a mano, extrayendolas del sitio de Google Maps una a una. Es mas tedioso pero asegura que las coordenadas sean las mas exactas posibles.

Aunque hay algunos mapas libres, no dan las coordenadas exactas, y otros requieren una llave de la API *(API key)* para funcionar, y para que esta tenga alguna utilidad el desarrollador se ve obligado a pagar, como es el caso de Google Maps.
"""

class Station:

    def __init__(self):
        self.stations = {}
    '''
    Metodo para agregar las estaciones a un diccionario de datos. Se agrega el
    nombre de la estacion, junto a una lista que contiene el id que va a tener
    esta estacion y las coordenadas geograficas que tiene este lugar.
    Salida: 
        Guardar el resultado en el diccionario alojado en la presente clase.
    '''
    def build_all_stations(self):

        self.stations.setdefault('Portal Norte', [0, (4.754228, -74.046161)])
        self.stations.setdefault('Toberin', [1, (4.746185, -74.047279)])
        self.stations.setdefault('Calle 161', [2, (4.742706, -74.047863)])
        self.stations.setdefault('Mazuren', [3, (4.734499, -74.049242)]) 
        self.stations.setdefault('Calle 146', [4, (4.730832, -74.049868)]) 
        self.stations.setdefault('Calle 142', [5, (4.726947, -74.050305)]) 
        self.stations.setdefault('Alcala', [6, (4.720287, -74.051641)])
        self.stations.setdefault('Prado', [7, (4.713173, -74.052682)])
        self.stations.setdefault('Calle 127', [8, (4.704787, -74.054230)])
        self.stations.setdefault('Pepe Sierra', [9, (4.698795, -74.055251)])
        self.stations.setdefault('Calle 106', [10, (4.691557, -74.056421)])
        self.stations.setdefault('Calle 100', [11, (4.684800, -74.057570)])
        self.stations.setdefault('La Castellana', [12, (4.676243, -74.063387)])
        self.stations.setdefault('NQS-Calle 75', [13, (4.670653, -74.070593)])
        self.stations.setdefault('AV. Chile', [14, (4.665962, -74.074819)])
        self.stations.setdefault('Simon Bolivar', [15, (4.658008, -74.077797)])
        self.stations.setdefault('Movistar Arena', [16, (4.650119, -74.078363)])
        self.stations.setdefault('Campin - U. Antonio Nariño', [17, (4.644847, -74.078777)])
        self.stations.setdefault('AV. El Dorado', [18, (4.630541, -74.079891)])
        self.stations.setdefault('CAD', [19, (4.622983, -74.084559)])
        self.stations.setdefault('Paloquemao', [20, (4.617084, -74.089525)])
        self.stations.setdefault('Ricaurte', [21, (4.612523, -74.093075)])
        self.stations.setdefault('San Façon', [22, (4.609549, -74.086540)])
        self.stations.setdefault('De La Sabana', [23, (4.605659, -74.082138)])
        self.stations.setdefault('AV. Jiménez', [24, (4.603037, -74.079164)])
        self.stations.setdefault('Virrey', [25, (4.675857, -74.059144)])
        self.stations.setdefault('Calle 85', [26, (4.671851, -74.059702)])
        self.stations.setdefault('Héroes', [27, (4.668311, -74.060210)])
        self.stations.setdefault('Calle 76', [28, (4.664031, -74.061083)])
        self.stations.setdefault('Calle 72', [29, (4.659261, -74.061922)])
        self.stations.setdefault('Flores', [30, (4.654878, -74.063021)])
        self.stations.setdefault('Calle 63', [31, (4.648914, -74.064810)])
        self.stations.setdefault('Calle 57', [32, (4.642917, -74.065879)])
        self.stations.setdefault('Marly', [33, (4.636587, -74.066936)])
        self.stations.setdefault('Calle 45', [34, (4.632661, -74.067665)])
        self.stations.setdefault('AV. 39', [35, (4.627184, -74.068643)])
        self.stations.setdefault('Calle 34', [36, (4.621390, -74.069805)])
        self.stations.setdefault('Calle 26', [37, (4.616961, -74.072159)])
        self.stations.setdefault('Calle 22', [38, (4.611033, -74.075079)])
        self.stations.setdefault('Calle 19', [39, (4.608302, -74.076608)])
        self.stations.setdefault('Concejo de Bogotá', [40, (4.626496, -74.080722)])
        self.stations.setdefault('Centro Memoria', [41, (4.621915, -74.077436)])
        self.stations.setdefault('U. Nacional', [42, (4.636493, -74.079328)])
    '''
    Mide la distancia entre 2 coordenadas geograficas.
    Entradas:
        * frm: Coordenadas geograficas del sitio 1
        * to: Coordenadas geograficas del sitio 2
    Salida:
        La distancia en metros entre 2 puntos utilizando el algoritmo gran circulo
        de la libreria Geopy
    '''
    def distance(self, frm, to):
        
        return float(great_circle(frm, to).meters)

    '''
    Metodo que se encarga de crear las conexiones entre 2 estaciones en el grafo.
    Entradas:
        * frm: Coordenadas geograficas del sitio 1
        * to: Coordenadas geograficas del sitio 2
        * graph: Grafo de la clase graph
    '''
    def set_connections_stations(self, graph, frm, to):

        #Se obtienen los IDs de los nodos de incio y fin de la clase Vertex
        frm = vertex[self.stations[frm][0]]
        to = vertex[self.stations[to][0]]

        #Calcula el costo
        cost = self.distance(frm.get_coordinates(), to.get_coordinates())

        #Se agrega la conexion entre los nodos inicio y fin con su respectivo costo
        graph.add_edge(frm.get_id(), to.get_id(), cost)

    '''
    Dado un diccionario de datos y el id de un vertice devuelve el nombre de la estacion
    Entrada:
        * dictionary: Diccionaro de datos el cual contiene las estaciones
        * value: el id de la estacion, la cual se desea obtener el nombre.
    Salida:
        Retorna el nombre de la estacion. Si no se encontro retorna None.
    '''
    def get_station_by_id(self, dictionary, value):
        for s in dictionary:
            if dictionary[s][0] == value:
                return s
        return None

    '''
    Convierte una lista de IDs de nodos en el nombre de las estaciones que conforman
    la ruta mas optima dada por un algoritmo de busqueda no informada o informada.
    Entrada:
        * list_stations_id: Lista de la ruta optima que guarda el id de los nodos
    Salida:
        * Lista con los nombre de las estaciones que conforman la mejor ruta optima
    '''
    def convert_id_to_station(self, list_stations_id):
        new_list = []
        for id in list_stations_id:
            name_station = self.get_station_by_id(self.stations, id)
            new_list.append(name_station)
        return new_list

"""# **Inicializacion de objetos**

Para poder utilizar las funciones, crear y tener acceso al grafo y a las estaciones se procede a instanciar objetos de algunas clases vistas anteriormente.

> `g` sera el objeto del grafo, almacena el grafo y los vertices, ademas tiene las operaciones para agregar vertices y aristas con los pesos correspondientes.

> `s` va a ser el objeto para la clase `Station`, el cual contiene el diccionario con las estaciones a crear y las operaciones sobre estas estaciones.

Por ultimo, tenemos la variable `tree`, el cual actuara como instancia de la clase `TreeSearch`, y contendra todos los elementos para la busqueda de rutas mas cortas utilizando diferentes algoritmos informados y no informados.
"""

g = Graph()
s = Station()
tree = TreeSearch(g)

"""# **Construccion de las estaciones**

Mediante el metodo `build_all_stations` de la clase `Station` construimos todas las estaciones que vamos a utilizar y posteriormente guardandolas en el diccionario que se aloja en la anterior clase mencionada.

Por ultimo verificamos que todas las estaciones se hayan ingresado correctamente.
"""

s.build_all_stations()
s.stations

"""# **Agregar vertices al grafo**

Cada estacion es un estado del problema, por lo tanto cada estacion sera un vertice del grafo.

> Para lograr esto se añadira cada estacion como un vertice, apoyandonos en la funcion `add_vertex` de la clase `Graph` utilizando solamente el id de la estacion y las coordenadas que estan guardadas en el diccionario de estaciones.

Por ultimo se verifican que los vertices se hayan agregado correctamente y que se haya creado el diccionario correctamente guardando todos los ids en un nuevo diccionario de muestra.
"""

vertex = {}
#CREAR VERTICES
i = 0
for index in s.stations:
    v = g.add_vertex(s.stations[index][0], s.stations[index][1])
    #print(s.stations[index][0], s.stations[index][1])
    vertex.setdefault(i, v)
    i = i + 1

vertex

"""# **Impresion de las estaciones**

Para verificar que las estaciones e hayan agregado se imprime el id y el nombre de la estacion.
"""

for station in s.stations:
    print(s.stations[station][0], station)

"""# **Conectar estaciones**

Utilizando la funcion `Station.distance` para obtener el costo entre 2 estaciones y luego `Graph.add_edge` para conectar 2 vertices, se procede a crear las conexiones entre 2 estaciones con el metodo `Station.set_connections_stations`, pasandole como parametros el nombre de las 2 estaciones a conectar. Este metodo busca las estaciones y escoge el id de cada estacion para luego buscar su vertice correspondiente con este numero de identificacion qeu se aloja en el diccionario del grafo, conectandolos asi utilizando el objeto `g` de la clase `Graph.`.
"""

s.set_connections_stations(g, 'Portal Norte', 'Toberin')
s.set_connections_stations(g, 'Toberin', 'Calle 161')
s.set_connections_stations(g, 'Calle 161', 'Mazuren')
s.set_connections_stations(g, 'Mazuren', 'Calle 146')
s.set_connections_stations(g, 'Calle 146', 'Calle 142')
s.set_connections_stations(g, 'Calle 142', 'Alcala')
s.set_connections_stations(g, 'Alcala', 'Prado')
s.set_connections_stations(g, 'Prado', 'Calle 127')
s.set_connections_stations(g, 'Calle 127', 'Pepe Sierra')
s.set_connections_stations(g, 'Pepe Sierra', 'Calle 106')
s.set_connections_stations(g, 'Calle 106', 'Calle 100')
s.set_connections_stations(g, 'Calle 100', 'La Castellana')
s.set_connections_stations(g, 'La Castellana', 'NQS-Calle 75')
s.set_connections_stations(g, 'NQS-Calle 75', 'AV. Chile')
s.set_connections_stations(g, 'AV. Chile', 'Simon Bolivar')
s.set_connections_stations(g, 'Simon Bolivar', 'Movistar Arena')
s.set_connections_stations(g, 'Movistar Arena', 'Campin - U. Antonio Nariño')
s.set_connections_stations(g, 'Campin - U. Antonio Nariño', 'U. Nacional')
s.set_connections_stations(g, 'U. Nacional', 'AV. El Dorado')
s.set_connections_stations(g, 'AV. El Dorado', 'CAD')
s.set_connections_stations(g, 'CAD', 'Paloquemao')
s.set_connections_stations(g, 'Paloquemao', 'Ricaurte')
s.set_connections_stations(g, 'Ricaurte', 'San Façon')
s.set_connections_stations(g, 'San Façon', 'De La Sabana')
s.set_connections_stations(g, 'De La Sabana', 'AV. Jiménez')
s.set_connections_stations(g, 'Calle 100', 'Virrey')
s.set_connections_stations(g, 'Virrey', 'Calle 85')
s.set_connections_stations(g, 'Calle 85', 'Héroes')
s.set_connections_stations(g, 'Héroes', 'Calle 76')
s.set_connections_stations(g, 'Calle 76', 'Calle 72')
s.set_connections_stations(g, 'Calle 72', 'Flores')
s.set_connections_stations(g, 'Flores', 'Calle 63')
s.set_connections_stations(g, 'Calle 63', 'Calle 57')
s.set_connections_stations(g, 'Calle 57', 'Marly')
s.set_connections_stations(g, 'Marly', 'Calle 45')
s.set_connections_stations(g, 'Calle 45', 'AV. 39')
s.set_connections_stations(g, 'AV. 39', 'Calle 34')
s.set_connections_stations(g, 'Calle 34', 'Calle 26')
s.set_connections_stations(g, 'Calle 26', 'Calle 22')
s.set_connections_stations(g, 'Calle 22', 'Calle 19')
s.set_connections_stations(g, 'Calle 19', 'AV. Jiménez')
s.set_connections_stations(g, 'Calle 26', 'Centro Memoria')
s.set_connections_stations(g, 'Centro Memoria', 'Concejo de Bogotá')
s.set_connections_stations(g, 'Concejo de Bogotá', 'AV. El Dorado')
s.set_connections_stations(g, 'Concejo de Bogotá', 'CAD')

g.get_dictionary()

"""**Verificar Conexion**

Se imprime la creacion del grafo, la conexion entre cada nodo y su peso. Por ultimo se muestran los vertices adyacentes por cada vertice.
"""

for v in g:
    for w in v.get_connections():
        vid = v.get_id()
        wid = w.get_id()
        print ('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))

for v in g:
    print ('g.vert_dict[%s]=%s' %(v.get_id(), g.vert_dict[v.get_id()]))

"""# **Escoger estaciones de inicio y destino**

Imaginemos que vamos a realizar un viaje desde una estacion a otra. para este caso se ha elegido como inicio el Portal Norte hasta la AV. Jimenez (Nodo 0 y nodo 24 correspondientemente).

Para lograr esto obtenemos los nodos con la funcion `Graph.get_vertex` y los guardamos en una variable, lo que nos devolvera sera un objeto de la clase `Vertex`.
"""

node_from = g.get_vertex(0)
node_to = g.get_vertex(24)

"""# **Ejecucion de los algoritmos de busqueda**

Se procede a llamar a los metodos de busqueda alojados en la clase `TreeSearch`.

> Todos los metodos devuelven la ruta mas corta en forma de id de cada nodo. En el caso de A* devuelve un arreglo con la ruta optima y su costo acumulado. Para eliminar este costo se coge solamente la parte del id del nodo que corresponde la camino de la ruta mas optima decidida por este algoritmo.
"""

def delete_weights_dict(dictionary):
    for index, element in enumerate(dictionary):
        cad = element.split(':')
        node = cad[0]
        dictionary[index] = int(node)
    return dictionary

bfs = tree.bfs_shortest_path(node_from.get_id(), node_to.get_id())
ucs = tree.ucs(node_from, node_to)

tree.graph = g.get_dictionary()
dfs = tree.dfs_paths(node_from.get_id(), node_to.get_id())

tree.graph = g

heuristic = tree.construct_heristic(g, s)
a_star = tree.astar_search(g, heuristic, node_from.get_id(), node_to.get_id())
a_star = delete_weights_dict(a_star)

dijkstra = tree.astar_search(g, None, node_from.get_id(), node_to.get_id())
dijkstra = delete_weights_dict(dijkstra)

greedy = tree.astar_search(g, heuristic, node_from.get_id(), node_to.get_id(), gn = False)
greedy = delete_weights_dict(greedy)

#dijkstra = tree.a_star_search(g, node_from.get_id(), node_to.get_id(), heuris=False)

"""# **Conversion de id a nombre de la estacion**

Con el diccionario de estaciones podemos buscar que numero de identificacion tiene. Le pasamos la lista que contiene la ruta optima de cada algoritmo al metodo `Station.convert_id_to_station` para que nos devuelva la misma ruta pero con los nombres de la estacion.
"""

bfs_convert = s.convert_id_to_station(bfs)
ucs_convert = s.convert_id_to_station(ucs)
dfs_convert = s.convert_id_to_station(dfs)
astar_convert = s.convert_id_to_station(a_star)
dijkstra_convert = s.convert_id_to_station(dijkstra)
greedy_convert = s.convert_id_to_station(greedy)

"""# **Impresion de las rutas optimas por algoritmo**"""

print("BFS: " + str(bfs_convert))
print('UCS: ' + str(ucs_convert))
print("DFS: " + str(dfs_convert))
print('A*: ', astar_convert)
print('Dijkstra: ', dijkstra_convert)
print('Greedy: ', dijkstra_convert)

"""# **Conclusiones**
Como conclusiones se tiene que:

*   Aunque hayan multiples rutas, dependiendo de la necesidad del usuario cada algoritmo de busqueda puede dar una solucion diferente, la cual puede ser mas optima o no dependiendo de la persona.
*   Los algoritmos de busqueda no informada no son muy diferentes de las busquedas informadas. Los primeros hacen una busqueda a ciegas no tienen mucha informacion mas que el costo por cada conexion entre vertices, mientras que el segundo metodo tiene informacion anticipada, pudiendo tomar mejores decision estre escoger multiples estados en el mundo del problema.
*   El uso de busqueda se puede utilizar en multiples campos, no solo en geolocalizacion y busqueda de una mejor ruta en un mapa dentro de distintas localizaciones

# **Otros usos**

Este proyecto se puede utilizan en diferentes campos de accion, Como en este caso, en geolocalizacion o utilizando otras localizaciones, no necesariamente estaciones, se puede llegar a un resultado con un optimo local o global por cada algoritmo.

Tambien se tiene el campo de juegos, en donde se pueden armar agentes inteligentes en un mundo 2D o 3D y que hagan una busqueda de  un objeto en un mundo multidimensional o bidimensional, haciendo que el juego sea mas realista o interactivo con el jugador, segun sea el caso.

En redes computaciones tiene mucho campo de accion, podrian dotar los equipos de red, como modems, routers, switches, APs para dedicir cual es la mejor ruta dentro de una red y decidir por que camino enviar los paquetes y datos con el menor costo posible.
"""