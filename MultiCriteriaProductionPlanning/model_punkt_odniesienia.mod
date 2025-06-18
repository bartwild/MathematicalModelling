# Zbiór funkcji celu
set CELE := {1, 2, 3, 4, 5};  # 1-zysk, 2-emisja, 3-koszty, 4-zu¿ycie S1, 5-zu¿ycie S2
# Zmienne decyzyjne
var x1 >= 3 ; # Liczba sztuk produktu P1
var x2 >= 0 ; # Liczba sztuk produktu P2
var x3 >= 5 ; # Liczba sztuk produktu P3
# Funkcje celu
var f {i in CELE} = 
  if i = 1 then 9*x1 + 19*x2 + 9*x3
  else if i = 2 then 1*x1 + 1*x2 + 3*x3
  else if i = 3 then 1*x1 + 3*x2 + 3*x3
  else if i = 4 then 2*x1 + 10*x2 + 4*x3
  else 8*x1 + 1*x2 + 4*x3;  # zu¿ycie sk³adnika S2
# Punkty odniesienia
param r {CELE};  # punkty rezerwacji
param a {CELE};  # punkty aspiracji
# Parametry kontroluj¹ce kszta³t funkcji osi¹gniêcia - indywidualne dla ka¿dej funkcji celu
param gamma {CELE} default 1.2; # parametr gamma
param beta {CELE} default 0.8;  # parametr beta
# Inicjalizacja punktów odniesienia
data;
#param beta := 4 0.0 5 0.0;
#param gamma := 4 0.0 5 0.0;
param r :=
  1 130  # punkt rezerwacji dla zysku
  2 35   # punkt rezerwacji dla emisji
  3 80   # punkt rezerwacji dla kosztów
  4 110 # punkt rezerwacji dla zu¿ycia S1 
  5 55;  # punkt rezerwacji dla zu¿ycia S2 
param a :=
  1 150  # punkt aspiracji dla zysku
  2 30   # punkt aspiracji dla emisji
  3 70   # punkt aspiracji dla kosztów
  4 100  # punkt aspiracji dla zu¿ycia S1
  5  50; # punkt aspiracji dla zu¿ycia S2 
;
model;
# Zmienne pomocnicze dla funkcji osi¹gniêcia
var z {i in CELE}; # znormalizowane odleg³oœci dla ka¿dej funkcji celu
var min_z;         # minimalna znormalizowana odleg³oœæ
# Ograniczenia
subject to ogr_S1: 2*x1 + 10*x2 + 4*x3 <= 110;
subject to ogr_S2: 8*x1 + 1*x2 + 4*x3 <= 55;
subject to ogr_S3: 4*x1 + 0*x2 + 2*x3 <= 50;
# Definicje znormalizowanych odleg³oœci
subject to def_z_gamma {i in CELE}: 
  z[i] <= gamma[i] * (f[i] - r[i])/(a[i] - r[i]);
subject to def_z_normal {i in CELE}: 
  z[i] <= (f[i] - r[i])/(a[i] - r[i]);
subject to def_z_beta {i in CELE}: 
  z[i] <= beta[i] * (f[i] - a[i])/(a[i] - r[i]) + 1;
# Definicja minimalnej odleg³oœci
subject to min_z_def {i in CELE}: 
  min_z <= z[i];
# Funkcja celu - maksymalizacja minimalnej odleg³oœci + suma wa¿ona
param epsilon := 0.001;
maximize achievement: min_z + epsilon * sum {i in CELE} z[i];

