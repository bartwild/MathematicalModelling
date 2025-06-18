# Zbiory
set TYPES;
set MONTHS ordered;

# Parametry
param sell_price>=0;        # cena sprzeda¿y produktu [z³/tonê]
param stor_cost>=0;         # koszt magazynowania [z³/tonê]
param stor_cap>=0;          # maksymalny stan magazynowy [ton]
param init_inv {TYPES}>=0;  # pocz¹tkowy stan magazynowy dla ka¿dego rodzaju [ton]

# Ceny surowego oleju (œrednie) – miesi¹c Jan i Feb
param price {TYPES, MONTHS}>=0;

# Limity rafinacji:
param cap_plant>=0;   		# oleje roœlinne: A, B
param cap_nonplant>=0; 	 	# olej nieroœlinny: C
param M>=0;  				# du¿a sta³a
param hardness {TYPES}>=0; 	# Wspó³czynnik twardoœci

# Zmienna pomocnicza – ca³kowita produkcja w miesi¹cu m
var tot {MONTHS} >= 0;
# Zmienne decyzyjne:
var y {TYPES, MONTHS} binary;              # u¿ycie oleju w rafinacji
var b {TYPES, MONTHS} >= 0;                # zakup surowego oleju
var x {TYPES, MONTHS} >= 0;                # iloœæ rafinowanego oleju
var s {TYPES, MONTHS} >= 0, <= stor_cap;   # stan magazynowy


subject to TotalProduction {m in MONTHS}:
    tot[m] = sum {t in TYPES} x[t, m];
# Ograniczenie twardoœci produktu:
subject to Hardness {m in MONTHS}:
    (3 * tot[m] <= sum {t in TYPES} hardness[t] * x[t, m]) &&
    (sum {t in TYPES} hardness[t] * x[t, m] <= 6 * tot[m]);

# Bilans magazynowy:
subject to InvBalance {t in TYPES, m in MONTHS}:
    s[t, m] = (if m = first(MONTHS) then init_inv[t] else s[t, prev(m)]) + b[t, m] - x[t, m];

# Ograniczenia rafinacji:
subject to RefinePlant {m in MONTHS}:
    x["A", m] + x["B", m] <= cap_plant;

subject to RefineNonPlant {m in MONTHS}:
    x["C", m] <= cap_nonplant;

# Ograniczenie na 2 rodzaje oleju:
subject to AtMostTwoTypes {m in MONTHS}:
    sum {t in TYPES} y[t, m] <= 2;

# Powi¹zanie zmiennych x i y – jeœli olej t nie jest u¿yty, to x[t,m] musi byæ 0:
subject to LinkXY {t in TYPES, m in MONTHS}:
    x[t, m] <= M * y[t, m];

# Funkcja celu
maximize Profit:
    sell_price * sum {m in MONTHS}(tot[m])
    - sum {t in TYPES, m in MONTHS}(price[t, m] * b[t, m] + stor_cost * s[t, m]);

