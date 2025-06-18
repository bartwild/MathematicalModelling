# Zbiory
set NODES;                      # Zbi�r wszystkich w�z��w
set SOURCES within NODES;       # Zbi�r �r�de� (kopalnie)
set TRANS within NODES;         # Zbi�r w�z��w po�rednich (punkty prze�adunkowe)
set SINKS within NODES;         # Zbi�r uj�� (elektrownie)
set ARCS within {NODES, NODES}; # Zbi�r kraw�dzi (po��cze� transportowych)

# Parametry
param capacity {ARCS} >= 0;     # Maksymalna przepustowo�� kraw�dzi
param demand {SINKS} >= 0;      # Popyt w uj�ciach (elektrowniach)
param supply {SOURCES} >= 0;    # Poda� w �r�d�ach (kopalniach)
# Dodajemy super-�r�d�o i super-uj�cie
param super_source symbolic := 'S';
param super_sink symbolic := 'T';

# Zmienne decyzyjne
var flow {(i,j) in ARCS} >= 0, <= capacity[i,j]; # Przep�yw na kraw�dziach
var total_flow >= 0;                             # Ca�kowity przep�yw w sieci

# Funkcja celu - maksymalizacja przep�ywu
maximize Max_Flow: total_flow;

# Ograniczenia
# Przep�yw z super-�r�d�a
subject to Super_Source_Flow:
    sum {i in SOURCES} (sum {j in NODES: (i,j) in ARCS} flow[i,j]) = total_flow;

# Zachowanie przep�ywu w w�z�ach po�rednich
subject to Trans_Flow {i in TRANS}:
    sum {j in NODES: (i,j) in ARCS} flow[i,j] = sum {j in NODES: (j,i) in ARCS} flow[j,i];

# Przep�yw do super-uj�cia
subject to Super_Sink_Flow:
    sum {i in SINKS} (sum {j in NODES: (j,i) in ARCS} flow[j,i]) = total_flow;
    
# Zachowanie przep�ywu w w�z�ach uj�ciowych (elektrowniach)
subject to Sink_Flow {i in SINKS}:
    sum {j in NODES: (j,i) in ARCS} flow[j,i] >= demand[i];
    
    # Zachowanie przep�ywu w w�z�ach �r�d�owych (kopalniach)
subject to Source_Flow {i in SOURCES}:
    sum {j in NODES: (i,j) in ARCS} flow[i,j] <= supply[i];
    