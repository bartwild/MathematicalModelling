import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linear_sum_assignment

G = nx.DiGraph()
G.add_node('s', pos=(0, 3), node_color='lightgreen')
G.add_node('t', pos=(4, 3), node_color='lightcoral')
teams = ['A', 'B', 'C', 'D', 'E', 'F']
team_positions = {team: (1, 5.5 - i) for i, team in enumerate(teams)}
for team in teams:
    G.add_node(team, pos=team_positions[team], node_color='lightblue')
projects = ['1', '2', '3', '4', '5', '6']
project_positions = {proj: (3, 5.5 - i) for i, proj in enumerate(projects)}
for proj in projects:
    G.add_node(proj, pos=project_positions[proj], node_color='lightyellow')
for team in teams:
    G.add_edge('s', team, capacity="(1,0)")
for proj in projects:
    G.add_edge(proj, 't', capacity="(1,0)")

competencies = {
    ('A', '1'): "(1,15)", ('A', '3'): "(1, 11)", ('A', '5'): "(1, 13)", ('A', '6'): "(1, 11)",
    ('B', '2'): "(1, 12)", ('B', '3'): "(1, 14)", ('B', '4'): "(1, 16)",
    ('C', '1'): "(1, 14)", ('C', '2'): "(1, 16)", ('C', '4'): "(1, 11)", ('C', '5'): "(1, 17)",
    ('D', '1'): "(1, 9)", ('D', '3'): "(1, 12)", ('D', '5'): "(1, 13)",
    ('E', '2'): "(1, 10)", ('E', '4'): "(1, 12)", ('E', '6'): "(1, 16)",
    ('F', '1'): "(1, 12)", ('F', '5'): "(1, 15)", ('F', '6'): "(1, 18)"
}

for (team, proj), capacity in competencies.items():
    G.add_edge(team, proj, capacity=capacity)

plt.figure(figsize=(12, 10))
pos = nx.get_node_attributes(G, 'pos')
node_colors = [data.get('node_color', 'white') for _, data in G.nodes(data=True)]
nx.draw_networkx_nodes(G, pos, node_size=1500, node_color=node_colors, edgecolors='black')
nx.draw_networkx_edges(G, pos, width=1.5, arrowsize=15)
labels = {}
labels['s'] = 'Źródło s'
labels['t'] = 'Ujście t'
for team in teams:
    labels[team] = f'Zespół {team}'
for proj in projects:
    labels[proj] = f'Projekt {proj}'
nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
edge_labels = {(u, v): f"{d['capacity']}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, label_pos=0.12)
plt.title('Model sieciowy problemu przydziału zespołów do projektów', fontsize=15)
plt.axis('off')
plt.show()
cost_matrix = np.full((len(teams), len(projects)), np.inf)

for (team, proj), capacity_str in competencies.items():
    team_idx = teams.index(team)
    proj_idx = projects.index(proj)
    cost = int(capacity_str.split(',')[1].strip().rstrip(')'))
    cost_matrix[team_idx, proj_idx] = cost

row_ind, col_ind = linear_sum_assignment(cost_matrix)
optimal_flow = {}
for team in teams:
    optimal_flow[('s', team)] = 0
for proj in projects:
    optimal_flow[(proj, 't')] = 0
for team_idx, proj_idx in zip(row_ind, col_ind):
    if cost_matrix[team_idx, proj_idx] != np.inf:
        team = teams[team_idx]
        proj = projects[proj_idx]
        optimal_flow[('s', team)] = 1
        optimal_flow[(team, proj)] = 1
        optimal_flow[(proj, 't')] = 1

plt.figure(figsize=(12, 10))
G_solution = nx.DiGraph()
for node, data in G.nodes(data=True):
    G_solution.add_node(node, **data)
for u, v, data in G.edges(data=True):
    flow = optimal_flow.get((u, v), 0)
    G_solution.add_edge(u, v, capacity=data['capacity'], flow=flow)
nx.draw_networkx_nodes(G_solution, pos, node_size=1500, node_color=node_colors, edgecolors='black')
edges_with_flow = [(u, v) for u, v, d in G_solution.edges(data=True) if d['flow'] > 0]
edges_without_flow = [(u, v) for u, v, d in G_solution.edges(data=True) if d['flow'] == 0]
nx.draw_networkx_edges(G_solution, pos, edgelist=edges_with_flow, width=2.5, edge_color='red', arrowsize=15)
nx.draw_networkx_edges(G_solution, pos, edgelist=edges_without_flow, width=1, edge_color='gray', style='dashed', arrowsize=15)
nx.draw_networkx_labels(G_solution, pos, labels, font_size=8, font_weight='bold')
edge_labels = {(u, v): f"{d['flow']}/{d['capacity']}" for u, v, d in G_solution.edges(data=True)}
nx.draw_networkx_edge_labels(G_solution, pos, edge_labels=edge_labels, font_size=8, label_pos=0.12)

total_cost = 0
assignments = []
for team_idx, proj_idx in zip(row_ind, col_ind):
    if cost_matrix[team_idx, proj_idx] != np.inf:
        team = teams[team_idx]
        proj = projects[proj_idx]
        cost = int(cost_matrix[team_idx, proj_idx])
        total_cost += cost
        assignments.append((team, proj, cost))

plt.title(f'Optymalny przydział zespołów do projektów (Koszt całkowity: {total_cost})', fontsize=15)

assignment_text = "Optymalny przydział:\n"
for team, proj, cost in sorted(assignments):
    assignment_text += f"Zespół {team} → Projekt {proj} (koszt: {cost})\n"

plt.figtext(0.5, -0.05, assignment_text, ha="center", fontsize=12, bbox={"facecolor": "white", "alpha": 0.5, "pad": 5})
plt.axis('off')
plt.show()

print("Optymalny przydział zespołów do projektów:")
for team, proj, cost in sorted(assignments):
    print(f"Zespół {team} → Projekt {proj} (koszt: {cost})")
print(f"Całkowity koszt: {total_cost}")