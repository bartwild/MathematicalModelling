import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych z pliku CSV
df = pd.read_csv("pareto_results1.csv")
df_sorted = df.sort_values(by="Risk")
# Tworzenie wykresu – oś X: Ryzyko, oś Y: Oczekiwany zysk
plt.figure(figsize=(8, 6))
plt.plot(df_sorted["Risk"], df_sorted["ExpProfit"],
         marker='o', color='blue', label='Rozwiązania Pareto')

plt.xlabel("Ryzyko")

plt.ylabel("Oczekiwany zysk")
plt.title("Obraz zbioru rozwiązań efektywnych (Pareto)")
plt.legend()
plt.grid(True)
plt.show()
