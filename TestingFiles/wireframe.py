import math
class Node:
    # Constructor
    def __init__(self, coordinates):
        # Sets x, y, z of node from the coordinates passed in
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]


class Edge:
    # Constructor
    def __init__(self, start, stop):
        # Sets the coordinates of where the edge starts and stops
        self.start = start
        self.stop = stop


class Wireframe:
    # Constructor
    def __init__(self):
        # Stores the objects nodes and edges in an array
        self.nodes = []
        self.edges = []

    def addNodes(self, nodeList):
        # Takes in a list of nodes and add it to the object's node list
        for node in nodeList:
            self.nodes.append(Node(node))

    def addEdges(self, edgeList):
        for (start, stop) in edgeList:
            self.edges.append(Edge(self.nodes[start], self.nodes[stop]))

    def outputNodes(self):
        print("\n --- Nodes --- ")

        for i, node in enumerate(self.nodes):
            print(" %d: (%.2f, %.2f, %.2f)" % (i, node.x, node.y, node.z))


    def outputEdges(self):
        print("\n --- Edges --- ")

        for i, edge in enumerate(self.edges):
            print(" %d: (%.2f, %.2f, %.2f)" % (i, edge.start.x, edge.start.y, edge.start.z))

            print("to (%.2f, %.2f, %.2f)" % (edge.stop.x, edge.stop.y, edge.stop.z))


    def translate(self, axis, d):
        """ Add constant 'd' to the coordinate 'axis' of each node of a wireframe """

        if axis in ['x', 'y', 'z']:
            for node in self.nodes:
                setattr(node, axis, getattr(node, axis) + d)

    def scale(self, centre_x, centre_y, scale):
        """ Scale the wireframe from the centre of the screen """

        for node in self.nodes:
            node.x = centre_x + scale * (node.x - centre_x)
            node.y = centre_y + scale * (node.y - centre_y)
            node.z *= scale

    def findCentre(self):
        """ Find the centre of the wireframe. """
        num_nodes = len(self.nodes)
        meanX = sum([node.x for node in self.nodes]) / num_nodes
        meanY = sum([node.y for node in self.nodes]) / num_nodes
        meanZ = sum([node.z for node in self.nodes]) / num_nodes
        return (meanX, meanY, meanZ)

    def rotateZ(self, cx, cy, cz, radians):
        # Takes in the coordinates offset required to rotate cube
        # Rotates every node in node list using trig
        for node in self.nodes:
            # Calculates new offset for each node
            x = node.x - cx
            y = node.y - cy
            d = math.hypot(y, x)
            theta = math.atan2(y, x) + radians
            node.x = cx + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)
# Same concept but rotations in different axis
    def rotateX(self, cx, cy, cz, radians):
        for node in self.nodes:
            y = node.y - cy
            z = node.z - cz
            d = math.hypot(y, z)
            theta = math.atan2(y, z) + radians
            node.z = cz + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)

    def rotateY(self, cx, cy, cz, radians):
        for node in self.nodes:
            x = node.x - cx
            z = node.z - cz
            d = math.hypot(x, z)
            theta = math.atan2(x, z) + radians
            node.z = cz + d * math.cos(theta)
            node.x = cx + d * math.sin(theta)


if __name__ == "__main__":
    cube_nodes = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    cube = Wireframe()
    cube.addNodes(cube_nodes)
    cube.addEdges([(n, n + 4) for n in range(0, 4)])
    cube.addEdges([(n, n + 1) for n in range(0, 8, 2)])
    cube.addEdges([(n, n + 2) for n in (0, 1, 4, 5)])

    cube.outputNodes()
    cube.outputEdges()