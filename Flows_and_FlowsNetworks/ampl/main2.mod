# Zbiory
set TEAMS;    # Zbiór zespo³ów
set PROJECTS; # Zbiór projektów

# Parametry
param time {TEAMS, PROJECTS} default Infinity; # Czas realizacji projektu przez zespó³ (w miesi¹cach)

# Zmienne decyzyjne
var assign {TEAMS, PROJECTS} binary; # 1 jeœli zespó³ i realizuje projekt j, 0 w przeciwnym przypadku

# Funkcja celu - minimalizacja sumy czasów realizacji wszystkich projektów
minimize Total_Time: sum {i in TEAMS, j in PROJECTS: time[i,j] < Infinity} time[i,j] * assign[i,j];

# Ograniczenia
# Ka¿dy zespó³ realizuje co najwy¿ej jeden projekt
subject to One_Project_Per_Team {i in TEAMS}:
    sum {j in PROJECTS} assign[i,j] <= 1;

# Ka¿dy projekt jest realizowany przez dok³adnie jeden zespó³
subject to One_Team_Per_Project {j in PROJECTS}:
    sum {i in TEAMS} assign[i,j] = 1;

 