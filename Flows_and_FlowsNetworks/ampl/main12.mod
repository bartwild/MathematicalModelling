# Zbiory
set NODES;                      # Zbiór wszystkich wêz³ów
set SOURCES within NODES;       # Zbiór Ÿróde³ (kopalnie)
set TRANS within NODES;         # Zbiór wêz³ów poœrednich (punkty prze³adunkowe)
set SINKS within NODES;         # Zbiór ujœæ (elektrownie)
set ARCS within {NODES, NODES}; # Zbiór krawêdzi (po³¹czeñ transportowych)

# Parametry
param capacity {ARCS} >= 0;     # Maksymalna przepustowoœæ krawêdzi
param demand {SINKS} >= 0;      # Popyt w ujœciach (elektrowniach)
param supply {SOURCES} >= 0;    # Poda¿ w Ÿród³ach (kopalniach)
# Dodajemy super-Ÿród³o i super-ujœcie
param super_source symbolic := 'S';
param super_sink symbolic := 'T';

# Zmienne decyzyjne
var flow {(i,j) in ARCS} >= 0, <= capacity[i,j]; # Przep³yw na krawêdziach
var total_flow >= 0;                             # Ca³kowity przep³yw w sieci

# Funkcja celu - maksymalizacja przep³ywu
maximize Max_Flow: total_flow;

# Ograniczenia
# Przep³yw z super-Ÿród³a
subject to Super_Source_Flow:
    sum {i in SOURCES} (sum {j in NODES: (i,j) in ARCS} flow[i,j]) = total_flow;

# Zachowanie przep³ywu w wêz³ach poœrednich
subject to Trans_Flow {i in TRANS}:
    sum {j in NODES: (i,j) in ARCS} flow[i,j] = sum {j in NODES: (j,i) in ARCS} flow[j,i];

# Przep³yw do super-ujœcia
subject to Super_Sink_Flow:
    sum {i in SINKS} (sum {j in NODES: (j,i) in ARCS} flow[j,i]) = total_flow;
    
# Zachowanie przep³ywu w wêz³ach ujœciowych (elektrowniach)
subject to Sink_Flow {i in SINKS}:
    sum {j in NODES: (j,i) in ARCS} flow[j,i] >= demand[i];
    
    # Zachowanie przep³ywu w wêz³ach Ÿród³owych (kopalniach)
subject to Source_Flow {i in SOURCES}:
    sum {j in NODES: (i,j) in ARCS} flow[i,j] <= supply[i];
    