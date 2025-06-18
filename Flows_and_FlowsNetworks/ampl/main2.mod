# Zbiory
set TEAMS;    # Zbi�r zespo��w
set PROJECTS; # Zbi�r projekt�w

# Parametry
param time {TEAMS, PROJECTS} default Infinity; # Czas realizacji projektu przez zesp� (w miesi�cach)

# Zmienne decyzyjne
var assign {TEAMS, PROJECTS} binary; # 1 je�li zesp� i realizuje projekt j, 0 w przeciwnym przypadku

# Funkcja celu - minimalizacja sumy czas�w realizacji wszystkich projekt�w
minimize Total_Time: sum {i in TEAMS, j in PROJECTS: time[i,j] < Infinity} time[i,j] * assign[i,j];

# Ograniczenia
# Ka�dy zesp� realizuje co najwy�ej jeden projekt
subject to One_Project_Per_Team {i in TEAMS}:
    sum {j in PROJECTS} assign[i,j] <= 1;

# Ka�dy projekt jest realizowany przez dok�adnie jeden zesp�
subject to One_Team_Per_Project {j in PROJECTS}:
    sum {i in TEAMS} assign[i,j] = 1;

 