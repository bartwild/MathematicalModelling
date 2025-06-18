# Zbiory
set NODES;                      # Zbiór wszystkich wêz³ów
set SOURCES within NODES;       # Zbiór Ÿróde³ (kopalnie)
set TRANS within NODES;         # Zbiór wêz³ów poœrednich (punkty prze³adunkowe)
set SINKS within NODES;         # Zbiór ujœæ (elektrownie)
set ARCS within {NODES, NODES}; # Zbiór krawêdzi (po³¹czeñ transportowych)

# Parametry
param cost {ARCS} >= 0;         # Koszt jednostkowy transportu
param capacity {ARCS} >= 0;     # Maksymalna przepustowoœæ krawêdzi
param supply {SOURCES} >= 0;    # Poda¿ w Ÿród³ach (kopalniach)
param demand {SINKS} >= 0;      # Popyt w ujœciach (elektrowniach)

# Zmienne decyzyjne
var flow {(i,j) in ARCS} >= 0, <= capacity[i,j]; # Przep³yw na krawêdziach

# Funkcja celu - minimalizacja kosztu transportu
minimize Total_Cost: sum {(i,j) in ARCS} cost[i,j] * flow[i,j];

# Ograniczenia
# Zachowanie przep³ywu w wêz³ach Ÿród³owych (kopalniach)
subject to Source_Flow {i in SOURCES}:
    sum {j in NODES: (i,j) in ARCS} flow[i,j] <= supply[i];

# Zachowanie przep³ywu w wêz³ach poœrednich (punktach prze³adunkowych)
subject to Trans_Flow {i in TRANS}:
    sum {j in NODES: (i,j) in ARCS} flow[i,j] = sum {j in NODES: (j,i) in ARCS} flow[j,i];

# Zachowanie przep³ywu w wêz³ach ujœciowych (elektrowniach)
subject to Sink_Flow {i in SINKS}:
    sum {j in NODES: (j,i) in ARCS} flow[j,i] = demand[i];