import networkx as nx
import matplotlib.pyplot as plt

# Create the original graph
G = nx.DiGraph()
edges = [
    ("A", "D", {"cost": 3, "capacity": 8}),
    ("A", "E", {"cost": 6, "capacity": 10}),
    ("B", "D", {"cost": 6, "capacity": 10}),
    ("B", "E", {"cost": 3, "capacity": 13}),
    ("C", "D", {"cost": 4, "capacity": 10}),
    ("C", "E", {"cost": 5, "capacity": 8}),
    ("D", "E", {"cost": 2, "capacity": 20}),
    ("D", "F", {"cost": 5, "capacity": 16}),
    ("D", "G", {"cost": 7, "capacity": 6}),
    ("D", "H", {"cost": 3, "capacity": 10}),
    ("E", "F", {"cost": 5, "capacity": 7}),
    ("E", "G", {"cost": 4, "capacity": 4}),
    ("E", "H", {"cost": 2, "capacity": 2})
]
G.add_edges_from([(u, v, attr) for u, v, attr in edges])

# Add flow information to the graph
flow_data = [
    ("A", "D", 8),
    ("A", "E", 2),
    ("B", "D", 10),
    ("B", "E", 3),
    ("C", "D", 10),
    ("C", "E", 8),
    ("D", "E", 0),
    ("D", "F", 14),
    ("D", "G", 6),
    ("D", "H", 8),
    ("E", "F", 7),
    ("E", "G", 4),
    ("E", "H", 2)
]

# Update edge attributes with flow information
for u, v, flow in flow_data:
    G[u][v]['flow'] = flow
    G[u][v]['utilization'] = (flow / G[u][v]['capacity']) * 100

# Node positions
pos = {
    "A": (0.75, 1.5), "B": (0.75, 1), "C": (0.75, 0.5),
    "D": (1, 1.25), "E": (1, 0.75),
    "F": (1.25, 1.5), "G": (1.25, 1), "H": (1.25, 0.5)
}

# Create figure
plt.figure(figsize=(15, 10))

# Draw the graph
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=2000, arrowsize=40, font_weight='bold')

# Create edge labels with flow information
edge_labels = {(u, v): f"F:{d['flow']}/{d['capacity']}\nC:{d['cost']}" 
               for u, v, d in G.edges(data=True)}

# Draw edge labels
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                            font_size=15, label_pos=0.3)

# Color edges based on utilization
edges_to_draw = []
edge_colors = []
edge_widths = []

for u, v, d in G.edges(data=True):
    edges_to_draw.append((u, v))
    # Color based on utilization: red for high, green for low
    if d['flow'] == 0:
        edge_colors.append('lightgray')  # Unused edges
        edge_widths.append(1)
    elif d['utilization'] == 100:
        edge_colors.append('red')  # Fully utilized edges
        edge_widths.append(3)
    elif d['utilization'] > 50:
        edge_colors.append('orange')  # Moderately utilized edges
        edge_widths.append(2.5)
    else:
        edge_colors.append('green')  # Low utilization edges
        edge_widths.append(2)

# Draw edges with colors based on utilization
nx.draw_networkx_edges(G, pos, edgelist=edges_to_draw, 
                      edge_color=edge_colors, width=edge_widths)

# Add title with optimal cost
plt.title(f"", fontsize=16)

# Add legend
legend_elements = [
    plt.Line2D([0], [0], color='lightgray', lw=1, label='0%'),
    plt.Line2D([0], [0], color='green', lw=2, label='<50%'),
    plt.Line2D([0], [0], color='orange', lw=2.5, label='50-99%'),
    plt.Line2D([0], [0], color='red', lw=3, label='100%')
]
plt.legend(handles=legend_elements, loc='upper right')

# Add explanation of edge labels
plt.figtext(0.5, 0.01, "Etykiety: F:przepływ/przepustowość\nC: koszt jednostkowy", 
           ha="center", fontsize=12, bbox={"facecolor":"white", "alpha":0.5, "pad":5})

plt.axis('off')
plt.tight_layout()
plt.show()
