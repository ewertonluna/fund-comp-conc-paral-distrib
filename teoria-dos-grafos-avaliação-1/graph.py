from typing import Dict, Set, Tuple, Union
from edge_exception import EdgeException
from vortex import Vortex
from edge import Edge
from graph_exception import GraphException

class Graph:
	def __init__(self, is_directed=False):
		self.is_directed = is_directed
		self.vertices: Dict[str, Vortex] = dict()
		self.edges: Dict[str, Edge] = dict()
	
	def add_vortex(self, label: str):
		"""
		Adds vortex to the Graph

		Parameters:
		vortex_label (str): Label of the vortex
	
		Returns:
		None
	
		"""

		vortex = Vortex(label)
		self.vertices[vortex.label] = vortex
	
	def add_edge(self, label: str, connected_vertices: Union[Tuple[str, str], Set[str]], weight: float=0):
		"""
		Adds edge to the Graph

		Parameters:
		edge_label (str): Label of the edge
		connected_verties (tuple[str, str] | set(str)): A tuple (for directed graphs) or a set (for non-directed graphs)
			that represents the pair of vertices the edge connects.
	
		Returns:
		None
	
		"""

		non_existent_vertices = list()
		for vertice_label in connected_vertices:
			if not self.has_vertice(vertice_label):
				non_existent_vertices.append(vertice_label)

		if non_existent_vertices:
			raise GraphException(f"The edge is connected to one or more vertices that don't exist: (label(s): {non_existent_vertices})")

		edge = Edge(label, self.is_directed)
		try:
			edge.set_connected_vertices(connected_vertices)
			edge.set_weight(float(weight))
		except (EdgeException, ValueError) as e:
			raise GraphException('Error adding edge: ' + str(e))
		except Exception as e:
			raise GraphException('General exception:' + str(e))

		for vertice_label in connected_vertices:
			vortex = self.vertices[vertice_label]	
			vortex.add_adjacent_edge(edge)

		self.edges[edge.label] = edge
	
	def has_vertice(self, vortex_label: str) -> bool:
		"""
		Checks if the graph has a certain vertice

		Parameters:
		vortex_label (str): Label of the vortex
	
		Returns:
		bool: True if the vortex exists in the graph, False otherwise.
	
		"""

		return vortex_label in self.vertices.keys()
	

	def __repr__(self) -> str:
		repr = "Graph[\n" \
			f"\tis_directed: {self.is_directed}\n" \
			f"\tvertices: \n"

		for vortex in self.vertices.values():
			repr += f"\t\t{vortex}\n"

		repr += "\tedges:\n"

		for edge in self.edges.values():
			repr += f"\t\t{edge}\n"

		repr += "]"
		return repr
	

	def dijkstra(self, start_label: str):
		"""
		Performs dijkstra algorithm for a initial vortex returning the state of each vortex.

		Parameters:
		start_label (str): Label of the starting vortex 
	
		Returns:
		dict: A dictionary containing information about the cost from starting at the initial vortex
		to the vortex at that key. It also contains information of what is the previous vortex in the 
		path to get to the vortex at that key.

		For instance:
		The initial state, starting from vortex a, would be the following:
		dijkstra_data = {'a': {'cost': 0, 'previous_vortex': 'a', 'is_open': True}, 'b': {'cost': infinity, 'previous_vortex': None, 'is_open': True}}

		The final state would be the following. Note that the cost to get to b would be 3 coming from a:
		dijkstra_data = {'a': {'cost': 0, 'previous_vortex': 'a', 'is_open': True}, 'b': {'cost': 3, 'previous_vortex': 'a', 'is_open': True}}
		"""

		if self.is_directed:
			return self._dijkstra_for_directed(start_label)
		return self._dijkstra_for_non_directed(start_label)
	

	def get_shortest_path(self, start_label: str, end_label: str):
		"""
		Gets a list representing the path from the start vortex to the end vortex.

		Parameters:
		start_label (str): Label of the starting vortex 
		end_label (str): Label of the ending vortex 
	
		Returns:
		list: A list of the vertices labels that describes the path. If there's no path to get to the
		end vortex (infinite cost), returns an empty list.
	
		"""
		infinity = float("inf")
		dijkstra_data = self.dijkstra(start_label)
		shortest_path = list()

		current_label = end_label
		while current_label != start_label and dijkstra_data[current_label]['cost'] != infinity:
			shortest_path.append(current_label)
			current_label = dijkstra_data[current_label]['previous_vortex']

		if dijkstra_data[current_label]['cost'] != infinity:
			shortest_path.append(current_label)

		return shortest_path[::-1]
	

	def _dijkstra_for_non_directed(self, start_label: str):
		# Inicializando os valores: 
		# dijkstra_data = {'a': {'cost': 0, 'previous_vortex': 'a', 'is_open': True}, 'b': {'cost': -1, 'previous_vortex': None, 'is_open': True}}
		dijkstra_data = dict()
		infinity = float("inf")

		for label in self.vertices.keys():
			if label == start_label:
				dijkstra_data[label] = {'cost': 0, 'previous_vortex': label, 'is_open': True}
			else:
				dijkstra_data[label] = {'cost': infinity, 'previous_vortex': None, 'is_open': True}
		
		while self._has_open_vortex(dijkstra_data):
			# Escolhendo o vértice de menor custo
			label_of_min_cost = None
			min_cost = 0
			for label in dijkstra_data.keys():
				if dijkstra_data[label]['is_open']:
					if not label_of_min_cost and dijkstra_data[label]['cost'] != infinity:
						label_of_min_cost = label	
						min_cost = dijkstra_data[label]['cost']
					else:
						cost = dijkstra_data[label]['cost']
						if cost <= min_cost and cost != infinity:
							label_of_min_cost = label	
							min_cost = dijkstra_data[label]['cost']

			chosen_label = label_of_min_cost  # apenas renomeio a variável para ter um nome mais apropriado desse ponto em diante
			dijkstra_data[chosen_label]['is_open'] = False  # Fecha o vértice

			# Relaxando as arestas
			for adjacent_edge in self.vertices[chosen_label].adjacent_edges.values():  # adjacent_edges -> {'1': Edge1, '2': Edge2}, adjacent_edjes.values() -> [Edge1, Edge2, ...]
				edge_weight = adjacent_edge.weight
				vortex_label_1, vortex_label_2 = adjacent_edge.connected_vertices  # connected_vertices -> {'a', 'b'}
				opposite_vortex_label = vortex_label_1 if (vortex_label_1 != chosen_label) else vortex_label_2  # pega label do vértice conectado ao vértice escolhido

				if dijkstra_data[opposite_vortex_label]['is_open']:  # só faz o relaxamento se o vértice oposto estiver aberto
					if dijkstra_data[opposite_vortex_label]['cost'] == infinity:
						dijkstra_data[opposite_vortex_label]['cost'] = edge_weight + dijkstra_data[chosen_label]['cost']
						dijkstra_data[opposite_vortex_label]['previous_vortex'] = chosen_label
					else:
						if dijkstra_data[opposite_vortex_label]['cost'] >= edge_weight + dijkstra_data[chosen_label]['cost']:
							dijkstra_data[opposite_vortex_label]['cost'] = edge_weight + dijkstra_data[chosen_label]['cost']
							dijkstra_data[opposite_vortex_label]['previous_vortex'] = chosen_label

		return dijkstra_data
	

	def _dijkstra_for_directed(self, start_label: str):
		# Inicializando os valores: 
		# dijkstra_data = {'a': {'cost': 0, 'previous_vortex': 'a', 'is_open': True}, 'b': {'cost': -1, 'previous_vortex': None, 'is_open': True}}
		dijkstra_data = dict()
		infinity = float("inf")

		for label in self.vertices.keys():
			if label == start_label:
				dijkstra_data[label] = {'cost': 0, 'previous_vortex': label, 'is_open': True}
			else:
				dijkstra_data[label] = {'cost': infinity, 'previous_vortex': None, 'is_open': True}
		
		while self._has_open_vortex(dijkstra_data):
			# Escolhendo o vértice de menor custo
			label_of_min_cost = None
			min_cost = 0
			if self._has_only_infinite_cost_vertices_opened(dijkstra_data):
				for label in dijkstra_data.keys():
					if dijkstra_data[label]['is_open']:
						label_of_min_cost = label
						min_cost = dijkstra_data[label]['cost']
						break
			else:
				for label in dijkstra_data.keys():
					if dijkstra_data[label]['is_open']:
						if not label_of_min_cost and dijkstra_data[label]['cost'] != infinity:
							label_of_min_cost = label	
							min_cost = dijkstra_data[label]['cost']
						else:
							cost = dijkstra_data[label]['cost']
							if cost <= min_cost and cost != infinity:
								label_of_min_cost = label	
								min_cost = dijkstra_data[label]['cost']

			chosen_label = label_of_min_cost  # apenas renomeio a variável para ter um nome mais apropriado desse ponto em diante
			dijkstra_data[chosen_label]['is_open'] = False  # Fecha o vértice

			# Relaxando as arestas
			for adjacent_edge in self.vertices[chosen_label].adjacent_edges.values():  # adjacent_edges -> {'1': Edge1, '2': Edge2}
				edge_weight = adjacent_edge.weight
				_, vortex_label_2 = adjacent_edge.connected_vertices  # connected_vertices -> ('a', 'b')

				# só relaxa a aresta se ela estiver saindo do vértice escolhido:
				if vortex_label_2 != chosen_label:
					if dijkstra_data[vortex_label_2]['is_open']:  # só faz o relaxamento se o vértice oposto estiver aberto
						if dijkstra_data[vortex_label_2]['cost'] == infinity:
							dijkstra_data[vortex_label_2]['cost'] = edge_weight + dijkstra_data[chosen_label]['cost']
							dijkstra_data[vortex_label_2]['previous_vortex'] = chosen_label
						else:
							if dijkstra_data[vortex_label_2]['cost'] >= edge_weight + dijkstra_data[chosen_label]['cost']:
								dijkstra_data[vortex_label_2]['cost'] = edge_weight + dijkstra_data[chosen_label]['cost']
								dijkstra_data[vortex_label_2]['previous_vortex'] = chosen_label

		return dijkstra_data


	def _has_open_vortex(self, dijkstra_data) -> bool:
		has_open_vortex = False

		for value in dijkstra_data.values():
			if value['is_open']:
				has_open_vortex = True
				break
		return has_open_vortex

	
	def _has_only_infinite_cost_vertices_opened(self, dijkstra_data) -> bool:
		infinity = float("inf")
		has_only_infinite_cost_vertices = True

		for value in dijkstra_data.values():
			if value['is_open'] and value['cost'] != infinity:
				has_only_infinite_cost_vertices = False
				break
		return has_only_infinite_cost_vertices

# teste para método que retorna o menor caminho
# graph = Graph(True)
# graph.add_vortex('a')
# graph.add_vortex('b')
# graph.add_vortex('c')
# graph.add_vortex('d')
# graph.add_vortex('e')
# graph.add_edge('1', ('a', 'b'), 10)
# graph.add_edge('2', ('b', 'c'), 5)
# graph.add_edge('3', ('d', 'b'), 2)
# graph.add_edge('4', ('e', 'c'), 4)
# graph.add_edge('5', ('d', 'e'), 3)
# graph.add_edge('6', ('a', 'd'), 3)
# print(graph.get_shortest_path('a', 'c'))

	
# # teste para direcionado
# graph = Graph(True)
# graph.add_vortex('a')
# graph.add_vortex('b')
# graph.add_vortex('c')
# graph.add_vortex('d')
# graph.add_vortex('e')
# graph.add_edge('1', ('a', 'b'), 10)
# graph.add_edge('2', ('c', 'b'), 5)
# graph.add_edge('3', ('d', 'b'), 2)
# graph.add_edge('4', ('e', 'c'), 4)
# graph.add_edge('5', ('e', 'd'), 3)
# graph.add_edge('6', ('a', 'd'), 3)
# print(graph.dijkstra('b'))

# # teste para não direcionado
# graph = Graph()
# graph.add_vortex('a')
# graph.add_vortex('b')
# graph.add_vortex('c')
# graph.add_vortex('d')
# graph.add_vortex('e')
# graph.add_edge('1', {'a', 'b'}, 10)
# graph.add_edge('2', {'c', 'b'}, 5)
# graph.add_edge('3', {'d', 'b'}, 2)
# graph.add_edge('4', {'e', 'c'}, 4)
# graph.add_edge('5', {'d', 'e'}, 3)
# graph.add_edge('6', {'a', 'd'}, 3)
# print(graph.dijkstra('b'))