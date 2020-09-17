class Node(object):
    def __init__(self, value):
        self.value = value
        self.edges = []
        self.visited = False
