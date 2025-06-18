from amplpy import AMPL, add_to_path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

AMPL_MODEL = "main2.mod"
AMPL_DATA = "main2.dat"
add_to_path(r"E:\AMPL\ampl_mswin64")

ampl = AMPL()
ampl.read(AMPL_MODEL)
ampl.readData(AMPL_DATA)
ampl.setOption('solver', 'cplex')
ampl.setOption("solver_msg", 0)

w_profit_values = np.linspace(1, 1, 21)
w_risk_values = np.linspace(0, 200, 21)

results = []

for w_profit, w_risk in zip(w_profit_values, w_risk_values):
    ampl.getParameter("w_profit").set(w_profit)
    ampl.getParameter("w_risk").set(w_risk)
    ampl.solve()

    exp_profit = ampl.getVariable("ExpProfit").value()
    risk = ampl.getVariable("Risk").value()
    results.append({"w_profit": w_profit, "w_risk": w_risk, "ExpProfit": exp_profit, "Risk": risk})

df = pd.DataFrame(results)
df.to_csv("pareto_results2.csv", index=False)

print("✅ Analiza zakończona. Wyniki zapisano w pliku `pareto_results.csv`")
df_sorted = df.sort_values(by="Risk")

plt.figure(figsize=(8, 6))
plt.plot(df_sorted["Risk"], df_sorted["ExpProfit"],
         marker='o', color='blue', label='Rozwiązania Pareto')

plt.xlabel("Ryzyko")
plt.ylabel("Oczekiwany zysk")
plt.title("Obraz zbioru rozwiązań efektywnych (Pareto)")
plt.legend()
plt.grid(True)
plt.show()
