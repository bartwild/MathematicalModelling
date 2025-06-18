# Zbiory
set POINTS;  # Zbiór punktów sprzeda¿y

# Parametry
param base_plan {POINTS} >= 0;  # Plan bazowy dostaw
param total_base_plan := sum {i in POINTS} base_plan[i];  # Suma planu bazowego

# Zmienne decyzyjne
var delivery {i in POINTS} >= 0;  # Iloœæ produktu dostarczanego do punktu i
var pos_dev {i in POINTS} >= 0;   # Dodatnie odchylenie od planu bazowego
var neg_dev {i in POINTS} >= 0;   # Ujemne odchylenie od planu bazowego
var rel_dev {i in POINTS} >= 0;   # Wzglêdne odchylenie od planu bazowego
var max_rel_dev >= 0;             # Maksymalne wzglêdne odchylenie

# Funkcja celu - minimalizacja wa¿onej sumy maksymalnego odchylenia i sumy wszystkich odchyleñ
minimize Objective: max_rel_dev + 0.1 * sum {i in POINTS} rel_dev[i];

# Ograniczenia
# Definicja odchyleñ
subject to Deviation_Def {i in POINTS}:
    delivery[i] - base_plan[i] = pos_dev[i] - neg_dev[i];

# Definicja wzglêdnego odchylenia
subject to Rel_Dev_Def {i in POINTS}:
    rel_dev[i] = (pos_dev[i] + neg_dev[i]) / base_plan[i];

# Maksymalne wzglêdne odchylenie
subject to Max_Rel_Dev_Def {i in POINTS}:
    max_rel_dev >= rel_dev[i];

# Suma dostaw musi byæ równa sumie planu bazowego
subject to Total_Delivery:
    sum {i in POINTS} delivery[i] = total_base_plan;

# Ograniczenie 1: Suma towaru dostarczonego do punktów 1, 3, 8 ma byæ przynajmniej o 12% wiêksza ni¿ w planie bazowym
subject to Constraint_1:
    delivery[1] + delivery[3] + delivery[8] >= 1.12 * (base_plan[1] + base_plan[3] + base_plan[8]);

# Ograniczenie 2: Suma towaru dostarczonego do punktów 3, 5 ma byæ przynajmniej o 7% mniejsza ni¿ w planie bazowym
subject to Constraint_2:
    delivery[3] + delivery[5] <= 0.93 * (base_plan[3] + base_plan[5]);

# Ograniczenie 3: Iloœæ towaru dostarczonego do punktu 3 ma stanowiæ przynajmniej 80% towaru dostarczonego do punktu 7
subject to Constraint_3:
    delivery[3] >= 0.8 * delivery[7];
  
  
  
  
