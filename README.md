# SearchTransmilenioIA
Proyecto Transmilenio para buscar la mejor ruta entre multiples estaciones usando algoritmos de busqueda de Inteligencia Artificial progrmado en Python

## Descripcion
Este proyecto consiste en buscar la mejor ruta dentro del sistema de portales y estaciones de transmilenio. Para lograr esto se implementa un sistema de arboles y grafos para hacer busquedas no informadas e informadas con los algoritmos ```BSF, DFS, UCS, A*, Dijkstra y Greedy```
Para hacer la representacion sobre un grafo en computacion necesitamos construir varias clases que representen a los nodos, los pesos y la conexion entre ellos.

La principal ventaja es que un arbol es un tipo de grafo, por lo tanto nos serviran las mismas clases para representarlo.

Ademas de las clases se utilizo diccionarios, que es la manera mas facil de representar este tipo de estructuras de datos en Python. Claro, a este tipo de diccionarios van a guardar objetos de instancias de clases (Vertex) con el fin de almacenar multiples valores y datos en un mismo objeto, en vez de hacer multiples diccionarios, accion de programacion que es menos viable.

## Algoritmos

* **A*:** A estrella - A star
* **BFS:** Busqueda por anchura
* **DFS:** Busqueda por profundidad
* **UCS:** Busqueda por costo uniforme
* **Greedy:** Algoritmo Voraz
* **Dijkstra**

## Usos

Este proyecto se puede utilizan en diferentes campos de accion, Como en este caso, en geolocalizacion o utilizando otras localizaciones, no necesariamente estaciones, se puede llegar a un resultado con un optimo local o global por cada algoritmo.

Tambien se tiene el campo de juegos, en donde se pueden armar agentes inteligentes en un mundo 2D o 3D y que hagan una busqueda de  un objeto en un mundo multidimensional o bidimensional, haciendo que el juego sea mas realista o interactivo con el jugador, segun sea el caso.

En redes computaciones tiene mucho campo de accion, podrian dotar los equipos de red, como modems, routers, switches, APs para dedicir cual es la mejor ruta dentro de una red y decidir por que camino enviar los paquetes y datos con el menor costo posible.

## Requisitos y dependencias

Para la ejecucion de este proyecto requiere de ciertos parametros para poder ser ejecutado en un PC.

### Requisitos
Para poder ejecutar este proyecto correctamente se recomienda utilizar Python en su version 3 o superior.

Ademas de lo anterior, este proyecto utiliza geopy para poder utilizar ciertas metricas de medicion entre 2 estaciones utilizando las coordenadas terrestres. Para instalar esta libreria en su equipo de computo personal ejecute el siguiente comando en la terminal de comandos:

```
pip install geopy
```

#### Requerimientos del sistema
* **LENGUAJE:** Python Version 3 o superior
* **SISTEMA OPERATIVO:** Cualquiera compatible con Python (Windows, Linux, MacOS)
* **RED:** En caso de utilizar Google colab o similares requiere una conexion estable a Internet.

### Depedencias

* **Geopy:** Utilizado para medir distancias entre 2 coordenadas terrestres (latitud, longitud)

## Ejecucion

Para poder ejecutar este proyecto es necesario que haya instalado todas las dependencias en su PC. Ademas de esto, necesitara algunas herramientas para poder modificar y ejecutar el codigo en su equipo de computo. Estas herramientas se describen a continuacion:
* **Python:** El codigo de este proyecto esta bajo Python, es por ello que usted debe de instalar python en su dispositivo para ejecutar el codigo de este proyecto.
* **Jupyter:** Si lo que usted desea es ejecutar el codigo de este proyecto en su PC de manera local es necesario que tenga Jupyter instalado.
* **Google Colab:** No requiere instalacion. Si lo que usted quiere es ejecutar este proyecto de manera remota a traves de servidores, ahoorandose asi la descarga e instalacion de Python y jupyter puede utilizar Google Colab perfectamente. No necesita instalar nada, solamente tener un navegador web compatible con esta herramienta.

Si usted ha descargado el codigo en ```.py``: Para ejecutarlo necesita ejecutar el siguiente comando en la terminal de comandos de su sistema operativo correspondiente:
```
python transmilenio.py
```
**NOTA:** Posiblemente ejecutar el codigo en ```.py``` genere errores de ejecucion, puesto que el codigo ha sido programado utilizando Python Notebook (Google Colab)

## Construido con

* [Python](https://www.python.org/) - Lenguaje de programacion interpretado
* [GeoPy](https://geopy.readthedocs.io/en/stable/) - Libreria para manejo y medidas de distancia de ubicaciones y lugares terrestres.
* [Google Colab](https://research.google.com/colaboratory/faq.html) - IDE basado en Jupyter para crear programas en Python

## Autores

* **Carlos Garnica** - *Trabajo Inicial* - [Garnica1999](https://github.com/garnica1999)

También puedes mirar la lista de todos los [contribuyentes](https://github.com/Garnica1999/SearchTransmilenioIA/contributors) quíenes han participado en este proyecto. 

## Licencia

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE.md](https://github.com/Garnica1999/SearchTransmilenioIA/blob/master/LICENSE) para detalles
