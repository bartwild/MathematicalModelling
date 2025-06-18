# Pozosta³e zbiory, parametry i zmienne pozostaj¹ takie same jak w pierwszym modelu:
set TYPES;
set MONTHS ordered;
# Dodatkowe zbiory i parametry dla scenariuszy
set SCENARIOS;
param p {SCENARIOS} > 0;  # Prawdopodobieñstwa scenariuszy
# Uaktualniamy parametr price: dla ka¿dego rodzaju, miesi¹ca i scenariusza
param price {TYPES, MONTHS, SCENARIOS} >= 0;

param sell_price >= 0;
param stor_cost >= 0;
param stor_cap >= 0;
param init_inv {TYPES} >= 0;
param cap_plant >= 0;
param cap_nonplant >= 0;
param M >= 0;
param hardness {TYPES} >= 0;

var tot {MONTHS} >= 0;
var y {TYPES, MONTHS} binary;
var b {TYPES, MONTHS} >= 0;
var x {TYPES, MONTHS} >= 0;
var s {TYPES, MONTHS} >= 0, <= stor_cap;

subject to TotalProduction {m in MONTHS}:
    tot[m] = sum {t in TYPES} x[t, m];

subject to Hardness {m in MONTHS}:
    (3 * tot[m] <= sum {t in TYPES} hardness[t] * x[t, m]) &&
    (sum {t in TYPES} hardness[t] * x[t, m] <= 6 * tot[m]);

subject to InvBalance {t in TYPES, m in MONTHS}:
    s[t, m] = (if m = first(MONTHS) then init_inv[t] else s[t, prev(m)]) + b[t, m] - x[t, m];

subject to RefinePlant {m in MONTHS}:
    x["A", m] + x["B", m] <= cap_plant;

subject to RefineNonPlant {m in MONTHS}:
    x["C", m] <= cap_nonplant;

subject to AtMostTwoTypes {m in MONTHS}:
    sum {t in TYPES} y[t, m] <= 2;

subject to LinkXY {t in TYPES, m in MONTHS}:
    x[t, m] <= M * y[t, m];

# Definicja zysku dla ka¿dego scenariusza s:
var profit {SCENARIOS};
subject to ProfitDefinition {sc in SCENARIOS}:
    profit[sc] = sell_price * sum {m in MONTHS} tot[m]
                  - sum {t in TYPES, m in MONTHS} (price[t, m, sc] * b[t, m] + stor_cost * s[t, m]);

# Obliczenie oczekiwanego zysku:
var ExpProfit = sum {sc in SCENARIOS} p[sc] * profit[sc];

# Zmienne pomocnicze do obliczenia ró¿nicy Giniego bez u¿ycia abs()
var d {SCENARIOS, SCENARIOS} >= 0;

# Ograniczenia dla zmiennych pomocniczych
subject to DConstraint1 {sc1 in SCENARIOS, sc2 in SCENARIOS}:
    d[sc1, sc2] >= profit[sc1] - profit[sc2];

subject to DConstraint2 {sc1 in SCENARIOS, sc2 in SCENARIOS}:
    d[sc1, sc2] >= profit[sc2] - profit[sc1];
# Definicja miary ryzyka (œrednia ró¿nica Giniego) bez u¿ycia abs():
var Risk;
subject to GiniDefinition:
    Risk = (1/2) * sum {sc1 in SCENARIOS, sc2 in SCENARIOS} p[sc1] * p[sc2] * d[sc1, sc2];

# Metoda wa¿ona – ³¹czymy oba kryteria z wagami
param w_profit >= 0;
param w_risk >= 0;

# Funkcja celu – chcemy maksymalizowaæ zysk i minimalizowaæ ryzyko
#maximize MultiObjective:
#    w_profit * ExpProfit - w_risk * Risk;

param min_profit;

subject to MinProfitConstraint:
    ExpProfit >= min_profit;
    
# Zmiana funkcji celu na minimalizacjê ryzyka
minimize MinRiskOnly:
    Risk;