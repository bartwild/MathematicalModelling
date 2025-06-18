# Zbiory
set NODES;                      # Zbi�r wszystkich w�z��w
set SOURCES within NODES;       # Zbi�r �r�de� (kopalnie)
set TRANS within NODES;         # Zbi�r w�z��w po�rednich (punkty prze�adunkowe)
set SINKS within NODES;         # Zbi�r uj�� (elektrownie)
set ARCS within {NODES, NODES}; # Zbi�r kraw�dzi (po��cze� transportowych)

# Parametry
param cost {ARCS} >= 0;         # Koszt jednostkowy transportu
param capacity {ARCS} >= 0;     # Maksymalna przepustowo�� kraw�dzi
param supply {SOURCES} >= 0;    # Poda� w �r�d�ach (kopalniach)
param demand {SINKS} >= 0;      # Popyt w uj�ciach (elektrowniach)

# Zmienne decyzyjne
var flow {(i,j) in ARCS} >= 0, <= capacity[i,j]; # Przep�yw na kraw�dziach

# Funkcja celu - minimalizacja kosztu transportu
minimize Total_Cost: sum {(i,j) in ARCS} cost[i,j] * flow[i,j];

# Ograniczenia
# Zachowanie przep�ywu w w�z�ach �r�d�owych (kopalniach)
subject to Source_Flow {i in SOURCES}:
    sum {j in NODES: (i,j) in ARCS} flow[i,j] <= supply[i];

# Zachowanie przep�ywu w w�z�ach po�rednich (punktach prze�adunkowych)
subject to Trans_Flow {i in TRANS}:
    sum {j in NODES: (i,j) in ARCS} flow[i,j] = sum {j in NODES: (j,i) in ARCS} flow[j,i];

# Zachowanie przep�ywu w w�z�ach uj�ciowych (elektrowniach)
subject to Sink_Flow {i in SINKS}:
    sum {j in NODES: (j,i) in ARCS} flow[j,i] = demand[i];