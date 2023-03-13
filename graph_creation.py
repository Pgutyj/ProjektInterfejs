import networkx as nx
import matplotlib.pyplot as plt
l = []
x=0
G = nx.grid_2d_graph(13,11)
#tworzenie planszy/boiska
for i in range(1,11):
    for j in range(1,9):
        if j in range(4,6):
             l.append(((0,j),(0,j+1)))
             l.append(((12,j),(12,j+1)))
             l.append(((0,4),(1,4)))
             l.append(((11, 4), (12, 4)))
             l.append(((0, 6), (1, 6)))
             l.append(((11, 6), (12, 6)))
        l.append(((i,1),(i+1,1)))
        l.append(((i,9), (i+1, 9)))
        if j not in range(4,6):
            l.append(((1,j),(1,j+1)))
            l.append(((11,j),(11,j+1)))
#usuwanie krawędzie z pełnego grafu do pustego
G.remove_edges_from(G.edges())
#dodawanie krawędzi boiska
G.add_edges_from(l)
plt.figure(figsize=(18,18))
color_map=[]
for i in range(0,13):
    for j in range(0,11):
        if i == 0 or i==12:
            if j not in (4, 5, 6):
                color_map.append('#2DBC45')
            else:
                color_map.append('lightgreen')
        elif j == 0 or j == 10:
            color_map.append('#2DBC45')
        else:
            color_map.append('lightgreen')
outside = []
for i in range(0,13):
    for j in range(0,11):
        if j not in (4,5,6):
            outside.append((i,0))
            outside.append((i, 10))
            outside.append((0,j))
            outside.append((12, j))
# rysowanie grafu
pos = {(x, y): (y, -x) for x, y in G.nodes()}
def refresh_graph(G):
    G.remove_edges_from(G.edges())
    G.add_edges_from(l)
    pos = {(x, y): (y, -x) for x, y in G.nodes()}
    nx.draw(G, pos=pos,
        node_color=color_map,
        node_size=400)
    #wyświetlanie
    plt.show()
    #zapisanie do pliku
    plt.savefig("static/empty.png")
def D_SH_S(G, pos):
    nx.draw(G, pos=pos,
        node_color=color_map,
        node_size=400)
    #wyświetlanie
    plt.show()
    #zapisanie do pliku
    plt.savefig("static/empty.png")


