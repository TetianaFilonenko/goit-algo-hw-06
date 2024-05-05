import networkx as nx
import matplotlib.pyplot as plt


def dfs_paths(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal:
        yield path
    for next_node in set(graph.neighbors(start)) - set(path):
        yield from dfs_paths(graph, next_node, goal, path + [next_node])


def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in set(graph.neighbors(vertex)) - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))


# Створення пустого графа
G = nx.Graph()

# Додавання вершин (людей)
people = ["Олег", "Марія", "Андрій", "Наталія", "Іван", "Оксана"]
G.add_nodes_from(people)

# Додавання ребер з вагами, де ваги - дистанція в км між людьми
friendships = [
    ("Олег", "Марія", 1),
    ("Олег", "Андрій", 2),
    ("Олег", "Наталія", 3),
    ("Марія", "Наталія", 2),
    ("Наталія", "Іван", 4),
    ("Іван", "Оксана", 1),
    ("Марія", "Оксана", 3),
    ("Андрій", "Оксана", 2),
]
G.add_weighted_edges_from(friendships)

# Знаходження шляхів від Олега до Івана
dfs_result = list(dfs_paths(G, "Олег", "Іван"))[0]
bfs_result = list(bfs_paths(G, "Олег", "Іван"))[0]

# Візуалізація графа
pos = nx.spring_layout(G)

fig, ax = plt.subplots(2, 2, figsize=(15, 10))  # Створення фігури з двома підграфіками

# Підграфік 1: Візуалізація графа
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightblue",
    node_size=2000,
    edge_color="gray",
    width=2,
    ax=ax[0, 0],
)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax[0, 0])
ax[0, 0].set_title("Соціальна мережа")

# Вивід тексту з характеристиками графа
degrees = G.degree()
degree_str = ', '.join(f"{person} ({degree})" for person, degree in degrees)

textstr = "\n".join(
    [
        f"Кількість людей: {G.number_of_nodes()}",
        f"Кількість дружніх відносин: {G.number_of_edges()}",
        f"Ступені вершин: {degree_str}",
        f"Середня кількість друзів на людину: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}",
    ]
)

fig.text(
    0.5,
    0.95,
    textstr,
    ha="center",
    va="center",
    fontsize=10,
    bbox={"facecolor": "white", "alpha": 0.5, "pad": 10},
)


# Підграфік 2: Візуалізація шляху DFS
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightblue",
    edge_color="gray",
    width=2,
    node_size=2000,
    ax=ax[0, 1],
)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=[(dfs_result[i], dfs_result[i + 1]) for i in range(len(dfs_result) - 1)],
    width=3,
    edge_color="red",
    ax=ax[0, 1],
)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax[0, 1])
ax[0, 1].set_title("Шлях DFS від Олега до Івана")

# Підграфік 3: Візуалізація шляху BFS
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightblue",
    node_size=2000,
    edge_color="gray",
    width=2,
    ax=ax[1, 0],
)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=[(bfs_result[i], bfs_result[i + 1]) for i in range(len(bfs_result) - 1)],
    width=3,
    edge_color="blue",
    ax=ax[1, 0],
)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax[1, 0])
ax[1, 0].set_title("Шлях BFS від Олега до Івана")


# Використання алгоритму Дейкстри для знаходження найкоротших шляхів
dijkstra_path = nx.dijkstra_path(G, "Олег", "Іван")

# Підграфік 4: Візуалізація шляху за алгоритмом Дейкстри
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightblue",
    node_size=2000,
    edge_color="gray",
    width=2,
    ax=ax[1, 1],
)
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=list(zip(dijkstra_path[:-1], dijkstra_path[1:])),
    edge_color="green",
    width=3,
    ax=ax[1, 1],
)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax[1, 1])
ax[1, 1].set_title("Найкоротший шлях від Олега до Івана за Дейкстрою")

plt.tight_layout()
plt.show()
