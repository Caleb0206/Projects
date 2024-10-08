from stack_array import * #Needed for Depth First Search
from queue_array import * #Needed for Breadth First Search

class Vertex:
    '''Add additional helper methods if necessary.'''
    def __init__(self, key):
        '''Add other Attributes as necessary'''
        self.id = key
        self.adjacent_to = []


class Graph:
    '''Add additional helper methods if necessary.'''
    def __init__(self, filename):
        '''reads in the specification of a graph and creates a graph using an adjacency list representation.  
           You may assume the graph is not empty and is a correct specification.  E.g. each edge is 
           represented by a pair of vertices.  Note that the graph is not directed so each edge specified 
           in the input file should appear on the adjacency list of each vertex of the two vertices associated 
           with the edge.'''
        # This method should call add_vertex and add_edge!!!
        self.vertices = {}
        fileInput = open(filename, 'r')
        for line in fileInput.readlines():
            if len(line) > 0:
                pair = line.split()
                if len(pair) == 2:
                    self.add_vertex(pair[0])
                    self.add_vertex(pair[1])
                    self.add_edge(pair[0], pair[1])

        fileInput.close()


    def add_vertex(self, key):
        # Should be called by init
        '''Add vertex to graph only if the vertex is not already in the graph.'''
        if key not in self.vertices:
            self.vertices[key] = Vertex(key)

    def add_edge(self, v1, v2):
        # Should be called by init
        '''v1 and v2 are vertex ID's. As this is an undirected graph, add an 
           edge from v1 to v2 and an edge from v2 to v1.  You can assume that
           v1 and v2 are already in the graph'''
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].adjacent_to.append(v2)
            self.vertices[v2].adjacent_to.append(v1)

    def get_vertex(self, key):
        '''Return the Vertex object associated with the ID. If ID is not in the graph, return None'''
        if key not in self.vertices:
            return None
        return self.vertices[key]

    def get_vertices(self):
        '''Returns a list of ID's representing the vertices in the graph, in ascending order'''
        return sorted(self.vertices.keys())

    def conn_components(self): 
        '''Return a Python list of lists.  For example: if there are three connected components 
           then you will return a list of three lists.  Each sub list will contain the 
           vertices (in ascending alphabetical order) in the connected component represented by that list.
           The overall list will also be in ascending alphabetical order based on the first item in each sublist.'''
        #This method MUST use Depth First Search logic!
        visited = set()
        overall_list = []
        stak = Stack(len(self.vertices))
        for val in self.get_vertices():
            vertex = self.get_vertex(val)
            if vertex not in visited:
                stak.push(vertex)
                visited.add(vertex)
                sublist = [vertex.id]

                while not stak.is_empty():
                    current_v = stak.peek()
                    found_unvisited = False

                    for adj_vert_key in current_v.adjacent_to:
                        adj_vertex = self.get_vertex(adj_vert_key)
                        if adj_vertex not in visited:
                            stak.push(adj_vertex)
                            visited.add(adj_vertex)
                            sublist.append(adj_vertex.id)
                            found_unvisited = True

                    if not found_unvisited:
                        stak.pop()

                sorted_sublist = sorted(sublist)
                overall_list.append(sorted_sublist)
        overall_list.sort(key=lambda x: x[0])
        return overall_list


    def is_bipartite(self):
        '''Return True if the graph is bipartite, False otherwise.'''
        #This method MUST use Breadth First Search logic!
        # colors each vertex red or black

        redblack_colors = {}
        for key in self.vertices:
            if key not in redblack_colors:
                q = Queue(len(self.vertices))
                current_v = self.get_vertex(key)
                redblack_colors[key] = 'B'

                q.enqueue(current_v)
                while not q.is_empty():

                    root = q.dequeue()
                    for adj_key in root.adjacent_to:
                        adj_v = self.vertices[adj_key]

                        if adj_key not in redblack_colors:
                            redblack_colors[adj_key] = ''

                        if redblack_colors[root.id] == redblack_colors[adj_key]:
                            # returns false if the root and adjacent vertex have the same color
                            return False
                        if redblack_colors[root.id] == 'B' and redblack_colors[adj_key] == '':
                            # if root black and adjacent vertex already red, don't do anything
                            # only care about enqueuing a vertex with no color
                            redblack_colors[adj_key] = 'R'
                            q.enqueue(adj_v)
                        elif redblack_colors[root.id] == 'R' and redblack_colors[adj_key] == '':
                            redblack_colors[adj_key] = 'B'
                            q.enqueue(adj_v)




        return True

