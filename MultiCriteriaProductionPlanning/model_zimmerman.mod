# Model optymalizacji z wykorzystaniem podejścia Zimmermana dla zbiorów rozmytych

# Zmienne decyzyjne
var x1 >= 3 ; # Liczba sztuk produktu P1
var x2 >= 0 ; # Liczba sztuk produktu P2
var x3 >= 5 ; # Liczba sztuk produktu P3
# Funkcje celu
var zysk = 9*x1 + 19*x2 + 9*x3;        # Zysk (10-1)*x1 + (22-3)*x2 + (12-3)*x3
var emisja = 1*x1 + 1*x2 + 3*x3;        # Emisja zanieczyszczeń
var koszty = 1*x1 + 3*x2 + 3*x3;        # Koszty produkcji
var zuzycie_S1 = 2*x1 + 10*x2 + 4*x3;   # Zużycie surowca S1
var zuzycie_S2 = 8*x1 + 1*x2 + 4*x3;    # Zużycie surowca S2
# Ograniczenia zasobów
subject to ogr_S1: zuzycie_S1 <= 110;
subject to ogr_S2: zuzycie_S2 <= 55;
subject to ogr_S3: 4*x1 + 0*x2 + 2*x3 <= 50;
# Zmienna decyzyjna alfa - poziom satysfakcji
var alfa >= 0, <= 3;
# Funkcje przynależności dla poszczególnych celów
# μ_1 (Zysk) = (zysk - 130)/20 dla 130 ≤ zysk < 150, 0 dla zysk < 130, 1 dla zysk ≥ 150
subject to funkcja_przynaleznosci_zysk:
  alfa <= (zysk - 130)/20;
# μ_2 (Emisja) = (35 - emisja)/5 dla 30 ≤ emisja < 35, 1 dla emisja < 30, 0 dla emisja ≥ 35
#subject to funkcja_przynaleznosci_emisja:
#  alfa <= (35 - emisja)/5;
# μ_3 (Koszt) = (80 - koszty)/10 dla 70 ≤ koszty < 80, 1 dla koszty < 70, 0 dla koszty ≥ 80
subject to funkcja_przynaleznosci_koszty:
  alfa <= (80 - koszty)/10;
# μ_4 (Zużycie S1) = (110 - zuzycie_S1)/10 dla 100 ≤ zuzycie_S1 < 110, 1 dla zuzycie_S1 < 100,
# 0 dla zuzycie_S1 ≥ 110
#subject to funkcja_przynaleznosci_S1:
#  alfa <= (110 - zuzycie_S1)/10;
# μ_5 (Zużycie S2) = (55 - zuzycie_S2)/5 dla 50 ≤ zuzycie_S2 < 55, 1 dla zuzycie_S2 < 50, 0 dla zuzycie_S2 ≥ 55
#subject to funkcja_przynaleznosci_S2:
#  alfa <= (55 - zuzycie_S2)/5;
# Funkcja celu - maksymalizacja poziomu satysfakcji alfa
maximize poziom_satysfakcji: alfa;



