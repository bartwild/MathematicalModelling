import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

# --- DANE ---
# Oryginalne dane dla w=1 (niska waga ryzyka)
profits_w1 = np.array([
    122440, 124080, 123280, 122900, 124070, 123120, 123110, 122920, 122370, 122370,
    124910, 122560, 123130, 121910, 121950, 122230, 123340, 122200, 123180, 121560,
    124690, 123410, 122670, 124660, 122410, 122920, 123960, 122680, 123460, 123680,
    121560, 123770, 123100, 123100, 122280, 123970, 122220, 122590, 124350, 122620,
    123660, 123680, 123210, 123730, 122460, 122410, 122960, 123040, 123580, 124350,
    122850, 121470, 124390, 122840, 122180, 124930, 123470, 123810, 122320, 123440,
    122340, 122800, 123690, 122410, 122760, 122330, 121970, 122050, 123210, 121860,
    123190, 123360, 124110, 123720, 124640, 122950, 122210, 122430, 122200, 121900,
    122390, 122580, 124360, 123690, 123540, 122880, 123770, 123100, 124210, 122060,
    121330, 123820, 123810, 124310, 124280, 122910, 122940, 123120, 123070, 124590
])

# Dane dla w=10 (10x większa waga ryzyka)
profits_w10 = np.array([
    122393, 123938, 123304, 122853, 123916, 123002, 123051, 122849, 122287, 122311,
    124827, 122418, 123000, 121780, 121867, 122076, 123364, 122082, 123085, 121560,
    124536, 123327, 122635, 124542, 122304, 122825, 123842, 122609, 123365, 123633,
    121489, 123687, 123005, 123005, 122162, 123911, 122196, 122436, 124362, 122573,
    123589, 123562, 123127, 123647, 122436, 122493, 122842, 123064, 123556, 124244,
    122815, 121435, 124378, 122745, 122156, 124611, 123175, 123704, 122273, 123322,
    122198, 122753, 123536, 122375, 122665, 122271, 121887, 121991, 123245, 121765,
    123107, 123265, 124004, 123649, 124569, 122867, 122245, 122347, 122176, 121900,
    122260, 122533, 124313, 123536, 123422, 122856, 123687, 122911, 124127, 122036,
    121318, 123655, 123727, 124204, 124280, 122804, 122893, 122978, 123058, 124436
])

n_scenarios = len(profits_w1)
probability = 1.0 / n_scenarios
p_array = np.full(n_scenarios, probability)

# Obliczanie podstawowych statystyk
stats_w1 = {
    'mean': np.mean(profits_w1),
    'median': np.median(profits_w1),
    'std': np.std(profits_w1),
    'min': np.min(profits_w1),
    'max': np.max(profits_w1),
    'range': np.max(profits_w1) - np.min(profits_w1)
}

stats_w10 = {
    'mean': np.mean(profits_w10),
    'median': np.median(profits_w10),
    'std': np.std(profits_w10),
    'min': np.min(profits_w10),
    'max': np.max(profits_w10),
    'range': np.max(profits_w10) - np.min(profits_w10)
}

# Funkcja do obliczania dystrybuanty empirycznej
def compute_cdf(profits):
    sorted_indices = np.argsort(profits)
    sorted_profits = profits[sorted_indices]
    cdf = np.cumsum(p_array[sorted_indices])
    return sorted_profits, cdf

profits_w1_sorted, cdf_w1 = compute_cdf(profits_w1)
profits_w10_sorted, cdf_w10 = compute_cdf(profits_w10)

# Tworzenie wykresów
plt.figure(figsize=(15, 12))

# 1. Wykres dystrybuant
plt.subplot(2, 2, 1)
plt.step(profits_w1_sorted, cdf_w1, where='post', label='w=1 (niska waga ryzyka)', linestyle='-', color='b')
plt.step(profits_w10_sorted, cdf_w10, where='post', label='w=10 (wysoka waga ryzyka)', linestyle='--', color='r')
plt.xlabel('Profit')
plt.ylabel('F(z) = P(Y ≤ z)')
plt.title('Empiryczne dystrybuanty profitów')
plt.legend()
plt.grid(True)

# 2. Histogramy z nakładaniem
plt.subplot(2, 2, 2)
plt.hist(profits_w1, bins=20, alpha=0.5, label='w=1', color='b')
plt.hist(profits_w10, bins=20, alpha=0.5, label='w=10', color='r')
plt.xlabel('Profit')
plt.ylabel('Liczba scenariuszy')
plt.title('Histogramy profitów')
plt.legend()
plt.grid(True)

# 3. Wykresy pudełkowe (box plots)
plt.subplot(2, 2, 3)
box_data = [profits_w1, profits_w10]
box_labels = ['w=1', 'w=10']
box_plot = plt.boxplot(box_data, labels=box_labels, patch_artist=True)
colors = ['lightblue', 'lightcoral']
for patch, color in zip(box_plot['boxes'], colors):
    patch.set_facecolor(color)
plt.ylabel('Profit')
plt.title('Wykresy pudełkowe profitów')
plt.grid(True)

# 4. Wykres rozrzutu (scatter plot) - porównanie zysków dla tych samych scenariuszy
plt.subplot(2, 2, 4)
plt.scatter(profits_w1, profits_w10, alpha=0.5)
plt.plot([np.min(profits_w1), np.max(profits_w1)], [np.min(profits_w1), np.max(profits_w1)], 'k--', alpha=0.5)
plt.xlabel('Profit dla w=1')
plt.ylabel('Profit dla w=10')
plt.title('Porównanie profitów dla tych samych scenariuszy')
plt.grid(True)

# Dodanie tabeli ze statystykami
plt.figure(figsize=(10, 6))
stats_table = pd.DataFrame({
    'w=1': [stats_w1['mean'], stats_w1['median'], stats_w1['std'], stats_w1['min'], stats_w1['max'], stats_w1['range']],
    'w=10': [stats_w10['mean'], stats_w10['median'], stats_w10['std'], stats_w10['min'], stats_w10['max'], stats_w10['range']]
}, index=['Średnia', 'Mediana', 'Odchylenie std.', 'Minimum', 'Maksimum', 'Zakres'])

# Obliczanie różnic procentowych
stats_table['Różnica %'] = ((stats_table['w=10'] - stats_table['w=1']) / stats_table['w=1'] * 100).round(2)

# Wyświetlanie tabeli jako wykresu
plt.axis('off')
plt.table(cellText=stats_table.values.round(2),
          rowLabels=stats_table.index,
          colLabels=stats_table.columns,
          cellLoc='center',
          loc='center',
          bbox=[0.2, 0.2, 0.6, 0.6])
plt.title('Porównanie statystyk profitów dla różnych wag ryzyka', y=0.8)

# Obliczanie i wyświetlanie miar ryzyka
risk_w1 = np.mean([np.abs(profits_w1[i] - profits_w1[j]) for i in range(n_scenarios) for j in range(n_scenarios)]) / 2
risk_w10 = np.mean([np.abs(profits_w10[i] - profits_w10[j]) for i in range(n_scenarios) for j in range(n_scenarios)]) / 2

print(f"Miara ryzyka (średnia różnica Giniego) dla w=1: {risk_w1:.2f}")
print(f"Miara ryzyka (średnia różnica Giniego) dla w=10: {risk_w10:.2f}")
print(f"Zmiana ryzyka: {(risk_w10 - risk_w1) / risk_w1 * 100:.2f}%")

plt.tight_layout()
plt.show()