from graphlib import BedGraph
from graphlib import BedNode
from draw_graphics import Renderer
from rgbmatrix import graphics
import time

if __name__ == '__main__':
    n0 = BedNode(-1, [5], "A1", (5,7), occupied=True)
    n1 = BedNode(-1, [6], "A2", (15,7), occupied=True)
    n2 = BedNode(-1, [7], "A3", (25, 7), occupied=True)
    n3 = BedNode(-1, [8], "A4", (35, 7), occupied=True)
    n4 = BedNode(-1, [9,11], "  ", (45, 7), occupied=False)

    n5 = BedNode(-1, [0,6], "  ", (5, 24), occupied=False)
    n6 = BedNode(-1, [1,5,7], "  ", (15, 24), occupied=False)
    n7 = BedNode(-1, [2,6,8], "  ", (25, 24), occupied=False)
    n8 = BedNode(-1, [3,7,9], "  ", (35, 24), occupied=False)
    n9 = BedNode(-1, [8,4,10], "  ", (45, 24), occupied=False)

    n10 = BedNode(-1, [9,11], "  ", (57, 24), occupied=False)
    n11 = BedNode(-1, [4,10], "  ", (57, 7), occupied=False)

    node_lst = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11]

    floor = BedGraph()
    for n in node_lst:
        floor.add_node(n)
    floor.construct()

    floor.print_data()

    path = floor.getPath(0,10, len(node_lst))
    print(path)
    
    rend = Renderer()

    rend.process(floor)

    time.sleep(1000)