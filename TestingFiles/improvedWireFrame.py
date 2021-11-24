import math
import numpy
class Node:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]

class Wireframe:
    def __init__(self):
        # More efficient code
        self.nodes = numpy.zeros((0,4))
        self.edges = []

    def addNodes(self, node_array):
        ones_column = numpy.ones((len(node_array), 1))
        ones_added = numpy.hstack((node_array, ones_column))
        self.nodes = numpy.vstack((self.nodes, ones_added))

    def addEdges(self, edgeList):
        self.edges += edgeList

    # Updated
    def outputNodes(self):
        print("\n --- Nodes --- ")

        for i, (x, y, z, _) in enumerate(self.nodes):
            print("   %d: (%d, %d, %d)" % (i, x, y, z))


    def outputEdges(self):
        print("\n --- Edges --- ")

        for i, (node1, node2) in enumerate(self.edges):
            print("   %d: %d -> %d" % (i, node1, node2))

    def transform(self, matrix):
        """ Apply a transformation defined by a given matrix. """
        self.nodes = numpy.dot(self.nodes, matrix)

    def scale(self, center, matrix):
        """ Scale the wireframe from the centre of the screen """
        for i, node in enumerate(self.nodes):
            self.nodes[i] = center + numpy.matmul(matrix, node - center)

    def rotate(self, center, matrix):
        for i, node in enumerate(self.nodes):
            # Multiply rotation matrix and node position to create a rotated coordinate for every node
            self.nodes[i] = center + numpy.matmul(matrix, node - center)

    def translationMatrix(self, dx, dy, dz):
        """ Return matrix for translation along vector (dx, dy, dz). """

        return numpy.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [dx, dy, dz, 1]])

    def findCentre(self):

        mean = self.nodes.mean(axis=0)  # to take the mean of each col

        return mean






if __name__ == "__main__":
    cube = Wireframe()
    cube_nodes = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    cube.addNodes(numpy.array(cube_nodes))
    cube.addEdges([(n, n + 4) for n in range(0, 4)])
    cube.addEdges([(n, n + 1) for n in range(0, 8, 2)])
    cube.addEdges([(n, n + 2) for n in (0, 1, 4, 5)])
    cube.outputNodes()
    cube.outputEdges()