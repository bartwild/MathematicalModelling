from amplpy import AMPL, add_to_path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
AMPL_MODEL = "main3.mod"
AMPL_DATA = "main3.dat"
add_to_path(r"E:\AMPL\ampl_mswin64")
ampl = AMPL()
ampl.read(AMPL_MODEL)
ampl.readData(AMPL_DATA)
ampl.setOption('solver', 'cplex')
ampl.setOption("solver_msg", 0)
profit_values = np.linspace(99900.00, 123094.00, 2)[::-1]
results = []
for min_profit_val in profit_values:
    ampl.getParameter("min_profit").set(min_profit_val)
    ampl.solve()
    exp_profit = ampl.getVariable("ExpProfit").value()
    risk = ampl.getVariable("Risk").value()
    results.append({"MinProfit": min_profit_val, "ExpProfit": exp_profit, "Risk": risk})
    print(f"Min Profit: {min_profit_val:.2f}, Osiągnięty zysk: {exp_profit:.2f}, Ryzyko: {risk:.2f}, miara bezpieczeństwa: {ampl.getVariable('security').value():.2f}")
    # print(ampl.get_variable("profit").getValues())
df = pd.DataFrame(results)
df.to_csv("pareto_results1.csv", index=False)
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
