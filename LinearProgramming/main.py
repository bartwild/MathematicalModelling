import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Tworzenie grafu skierowanego
G = nx.DiGraph()

# Dodawanie węzłów
plants = ["W1", "W2"]
warehouses = ["M1", "M2", "M3"]
stores = ["S1", "S2", "S3", "S4"]
products = ["P1", "P2"]

# Dane o produkcji w zakładach
production = {
    "W1": {"P1": "19/61", "P2": "29/51"},
    "W2": {"P1": "113/113", "P2": "108/108"}
}

# Dane o zapotrzebowaniu w sklepach
store_demand = {
    "S1": {"P1": 25, "P2": 36},
    "S2": {"P1": 40, "P2": 36},
    "S3": {"P1": 36, "P2": 36},
    "S4": {"P1": 31, "P2": 29}
}

# Dodawanie węzłów z odpowiednimi typami
for p in plants:
    G.add_node(p, type="plant", production=production[p])
for w in warehouses:
    G.add_node(w, type="warehouse")
for s in stores:
    G.add_node(s, type="store", demand=store_demand[s])

# Dane z rozwiązania AMPL
# Przepływ x (z zakładów do magazynów)
x_flow = {
    ("W1", "M1", "P1"): 5,
    ("W1", "M1", "P2"): 0,
    ("W1", "M2", "P1"): 7,
    ("W1", "M2", "P2"): 0,
    ("W1", "M3", "P1"): 7,
    ("W1", "M3", "P2"): 29,
    ("W2", "M1", "P1"): 0,
    ("W2", "M1", "P2"): 0,
    ("W2", "M2", "P1"): 0,
    ("W2", "M2", "P2"): 0,
    ("W2", "M3", "P1"): 113,
    ("W2", "M3", "P2"): 108
}

# Przepływ y (z magazynów do sklepów)
y_flow = {
    ("M1", "S1", "P1"): 0,
    ("M1", "S2", "P1"): 0,
    ("M1", "S3", "P1"): 0,
    ("M1", "S4", "P1"): 5,
    ("M2", "S1", "P1"): 0,
    ("M2", "S2", "P1"): 0,
    ("M2", "S3", "P1"): 0,
    ("M2", "S4", "P1"): 7,
    ("M3", "S1", "P1"): 25,
    ("M3", "S2", "P1"): 40,
    ("M3", "S3", "P1"): 36,
    ("M3", "S4", "P1"): 19,
    ("M1", "S1", "P2"): 0,
    ("M1", "S2", "P2"): 0,
    ("M1", "S3", "P2"): 0,
    ("M1", "S4", "P2"): 0,
    ("M2", "S1", "P2"): 0,
    ("M2", "S2", "P2"): 0,
    ("M2", "S3", "P2"): 0,
    ("M2", "S4", "P2"): 0,
    ("M3", "S1", "P2"): 36,
    ("M3", "S2", "P2"): 36,
    ("M3", "S3", "P2"): 36,
    ("M3", "S4", "P2"): 29
}

# Dodawanie krawędzi dla przepływu x
for (p, w, r), flow in x_flow.items():
    if flow > 0:
        if G.has_edge(p, w):
            G[p][w]['weight'] += flow
            G[p][w]['label'] += f", {r}:{flow}"
        else:
            G.add_edge(p, w, weight=flow, label=f"{r}:{flow}", product=r)

# Dodawanie krawędzi dla przepływu y
for (w, s, r), flow in y_flow.items():
    if flow > 0:
        if G.has_edge(w, s):
            G[w][s]['weight'] += flow
            G[w][s]['label'] += f", {r}:{flow}"
        else:
            G.add_edge(w, s, weight=flow, label=f"{r}:{flow}", product=r)

# Informacje o magazynach
warehouse_info = {
    "M1": {"size": "small", "capacity": 5, "used": 5},
    "M2": {"size": "small", "capacity": 7, "used": 7},
    "M3": {"size": "modular", "modules": 19, "capacity": 266, "used": 257}
}

# Ustawienie pozycji węzłów
pos = {}
# Zakłady na lewo
pos["W1"] = (-2, 1)
pos["W2"] = (-2, -1)
# Magazyny w środku
pos["M1"] = (0, 1.5)
pos["M2"] = (0, 0)
pos["M3"] = (0, -1.5)
# Sklepy na prawo
pos["S1"] = (2, 1.5)
pos["S2"] = (2, 0.5)
pos["S3"] = (2, -0.5)
pos["S4"] = (2, -1.5)

# Rysowanie grafu
plt.figure(figsize=(14, 10))

# Rysowanie węzłów z różnymi kolorami dla różnych typów
node_colors = []
for node in G.nodes():
    if node in plants:
        node_colors.append('lightgreen')
    elif node in warehouses:
        node_colors.append('lightblue')
    else:  # stores
        node_colors.append('salmon')

# Rysowanie węzłów
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=6500)

# Rysowanie etykiet węzłów
plant_labels = {p: f"{p}\nProdukcja:\nP1: {production[p]['P1']}\nP2: {production[p]['P2']}" for p in plants}
warehouse_labels = {w: f"{w}\n{warehouse_info[w]['size']}\n{warehouse_info[w]['used']}/{warehouse_info[w]['capacity']}" for w in warehouses}
store_labels = {s: f"{s}\nZapotrzebowanie:\nP1: {store_demand[s]['P1']}\nP2: {store_demand[s]['P2']}" for s in stores}
node_labels = {**plant_labels, **warehouse_labels, **store_labels}
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=9)

# Rysowanie krawędzi z różnymi kolorami dla różnych produktów
edges_p1 = [(u, v) for u, v, d in G.edges(data=True) if 'P1' in d.get('label', '')]
edges_p2 = [(u, v) for u, v, d in G.edges(data=True) if 'P2' in d.get('label', '')]
edges_both = [(u, v) for u, v, d in G.edges(data=True) if 'P1' in d.get('label', '') and 'P2' in d.get('label', '')]

# Usuwanie krawędzi, które są w obu listach z pojedynczych list
edges_p1 = [e for e in edges_p1 if e not in edges_both]
edges_p2 = [e for e in edges_p2 if e not in edges_both]

# Rysowanie krawędzi
nx.draw_networkx_edges(G, pos, edgelist=edges_p1, edge_color='blue', width=1.5, arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=edges_p2, edge_color='red', width=1.5, arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=edges_both, edge_color='purple', width=2, arrows=True)

# Rysowanie etykiet krawędzi z pozycją 0.25 zamiast domyślnej 0.5
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, label_pos=0.25)

# Dodawanie legendy
plant_patch = mpatches.Patch(color='lightgreen', label='Zakłady')
warehouse_patch = mpatches.Patch(color='lightblue', label='Magazyny')
store_patch = mpatches.Patch(color='salmon', label='Sklepy')
p1_line = mpatches.Patch(color='blue', label='Produkt P1')
p2_line = mpatches.Patch(color='red', label='Produkt P2')
both_line = mpatches.Patch(color='purple', label='Oba produkty')

plt.legend(handles=[plant_patch, warehouse_patch, store_patch, p1_line, p2_line, both_line], 
           loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3)

# Dodawanie tytułu i informacji o kosztach
plt.title("Przepływ produktów w sieci dystrybucji\nCałkowity koszt: 1883 tys. zł (Magazynowanie: 386 tys. zł, Transport: 1497 tys. zł)")
plt.axis('off')
plt.tight_layout()
plt.savefig("network_flow.png", dpi=300, bbox_inches='tight')
plt.show()