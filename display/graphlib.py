from enum import Enum

class status(Enum):
    IDLE = 1
    MOVING = 2

class BedNode:

    def __init__(self, idx, adj, name, centroid, occupied=False):
        self.idx = idx
        self.adj = adj
        self.occupied = occupied
        self.name = name
        self.centroid = centroid
        self.status = status.IDLE
    
    def __repr__(self):
        return "<Node {} at [{}] {}>".format(self.name, self.idx, self.status)
    
    def set_idx(self, idx):
        self.idx = idx

class BedGraph:

    def __init__(self):
        self.bed_nodes = []
        self.adj_matrix = []


    def construct(self):
        adj_array = [ [] for i in range(len(self.bed_nodes))]

        for src_node in self.bed_nodes:
            for dest_idx in src_node.adj:
                if dest_idx not in adj_array[src_node.idx]:
                    adj_array[src_node.idx].append(dest_idx)

                if src_node.idx not in adj_array[dest_idx]:
                    adj_array[dest_idx].append(src_node.idx)

        self.adj_matrix = adj_array

    def add_node(self, node:BedNode):
        l = len(self.bed_nodes)
        node.set_idx(l)
        self.bed_nodes.append(node)

    def BFS(self, src, dest, v, pred, dist):
        adj = self.adj_matrix # adjacency matrix
        queue = []

        visited = [False for i in range(v)]

        for i in range(v):

            dist[i] = 1000000
            pred[i] = -1
        
        visited[src] = True
        dist[src] = 0
        queue.append(src)

        while (len(queue) != 0):
            u = queue[0]
            queue.pop(0)
            for i in range(len(adj[u])):
            
                if (visited[adj[u][i]] == False):
                    visited[adj[u][i]] = True
                    dist[adj[u][i]] = dist[u] + 1
                    pred[adj[u][i]] = u
                    queue.append(adj[u][i])

                    if (adj[u][i] == dest):
                        return True

        return False

    def getPath(self, src, dest, v):
        pred=[0 for i in range(v)]
        dist=[0 for i in range(v)]

        if (self.BFS(src, dest, v, pred, dist) == False):
            print("Given source and destination are not connected")

        # vector path stores the shortest path
        path = []
        crawl = dest
        path.append(crawl)
        
        while (pred[crawl] != -1):
            path.append(pred[crawl])
            crawl = pred[crawl]
        path.reverse()

        return path

    def getIdxFromName(self, name):
        for node in self.bed_nodes:
            if node.name == name:
                return node.idx

    def print_data(self):
        print(self.bed_nodes)
        print(self.adj_matrix)

