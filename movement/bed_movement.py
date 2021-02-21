from enum import Enum


class status(Enum):
        MOVING = 1
        BASE = 2
        STOWED = 3

class Node:
    idx = -1
    adj = []
    available = True
    status  = -1
    
    def __init__(self, idx, adj, available=True):
        self.idx = idx
        self.adj = adj
        self.available = available
        self.status = status.STOWED
    
    def __str__(self):
        return "<Node idx [{}] {}>".format(self.idx, self.status)

    def __repr__(self):
        return "<Node idx [{}] {}>".format(self.idx, self.status)


def add_edge(adj_array, src_node : Node, dest_node : Node):
    
    if dest_node.idx not in adj_array[src_node.idx]:
        adj_array[src_node.idx].append(dest_node.idx)

    if src_node.idx not in adj_array[dest_node.idx]:
        adj_array[dest_node.idx].append(src_node.idx)

def construct_graph(node_list):
    adj_array = [ [] for i in range(len(node_list))]
    
    for node in node_list:
        if node.available:
            for adj_idx in node.adj:
                if node_list[adj_idx].available:
                    add_edge(adj_array, node, node_list[adj_idx])
    
    return adj_array

def BFS(adj, src, dest, v, pred, dist):

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

def printShortestDistance(adj, src, dest, v):
	
	pred=[0 for i in range(v)]
	dist=[0 for i in range(v)]

	if (BFS(adj, src, dest, v, pred, dist) == False):
		print("Given source and destination are not connected")

	# vector path stores the shortest path
	path = []
	crawl = dest
	path.append(crawl)
	
	while (pred[crawl] != -1):
		path.append(pred[crawl])
		crawl = pred[crawl]
	

	# distance from source is in distance array
	print("Shortest path length is : " + str(dist[dest]), end = '')

	# printing path from source to destination
	print("\nPath is : ")
	
	for i in range(len(path)-1, -1, -1):
		print(path[i], end=' ')

if __name__=='__main__':
    n1 = Node(0, [1], available=True)
    n2 = Node(1, [0,2,4])
    n3 = Node(2, [1], available=False)
    n4 = Node(3, [4], available=False)
    n5 = Node(4, [1,3,5,6,7])
    n6 = Node(5, [4], available=False)
    n7 = Node(6, [4,7])
    n8 = Node(7, [4,6])

    node_list = [n1, n2, n3, n4, n5, n6, n7, n8]
    
    adj_arr = construct_graph(node_list)
    print(adj_arr)

    printShortestDistance(adj_arr, 0, 7, len(node_list))
