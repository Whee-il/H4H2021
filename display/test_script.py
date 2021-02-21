from graphlib import BedGraph
from graphlib import BedNode
from draw_graphics import Renderer
from rgbmatrix import graphics
import time

if __name__ == '__main__':
    n0 = BedNode(-1, [4], "A1", (5,7), occupied=True)
    n1 = BedNode(-1, [5], "A2", (15,7), occupied=True)
    n2 = BedNode(-1, [6], "A3", (25, 7), occupied=True)
    n3 = BedNode(-1, [7], "A4", (35, 7), occupied=True)
    n4 = BedNode(-1, [], "  ", (45, 7), occupied=False)

    n5 = BedNode(-1, [], "  ", (5, 24), occupied=False)
    n6 = BedNode(-1, [], "  ", (15, 24), occupied=False)
    n7 = BedNode(-1, [], "  ", (25, 24), occupied=False)
    n8 = BedNode(-1, [], "  ", (35, 24), occupied=False)
    n9 = BedNode(-1, [], "  ", (45, 24), occupied=False)

    n10 = BedNode(-1, [], "  ", (57, 24), occupied=False)
    n11 = BedNode(-1, [], "  ", (57, 7), occupied=False)

    node_lst = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11]

    floor = BedGraph()
    for n in node_lst:
        floor.add_node(n)

    floor.construct()

    floor.print_data()

    rend = Renderer()

    rend.process(floor)

    time.sleep(1000)