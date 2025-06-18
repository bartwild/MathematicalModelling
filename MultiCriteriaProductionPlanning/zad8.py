import numpy as np
import matplotlib.pyplot as plt

# Kryteria
criteria = ['Zysk (C)', 'Emisja (Z)', 'Koszt (K)', 'Zużycie S1', 'Zużycie S2']

#method1_values = [167, 23, 33, 76, 49]  # Zadanie 4
#method2_values = [186, 24, 36, 86, 50]  # Zadanie 4
#method3_values = [167, 23, 33, 76, 49]  # Zadanie 5

method1_values = [156.26, 22.43, 31.30, 70, 48]  # Zadanie 4
method2_values = [150, 22.10526, 30.31579, 67.0526, 48.1053]  # Zadanie 7
method3_values = [150, 22.10526, 30.31579, 67.0526, 48.105]  # Zadanie 5

# Poziomy aspiracji i rezerwacji zgodnie z danymi:
aspiration = {'Zysk (C)': 150, 'Emisja (Z)': 30, 'Koszt (K)': 70, 'Zużycie S1': 100, 'Zużycie S2': 50}
reservation = {'Zysk (C)': 130, 'Emisja (Z)': 35, 'Koszt (K)': 80, 'Zużycie S1': 110, 'Zużycie S2': 55}


def normalize(value, crit):
    a = aspiration[crit]
    r = reservation[crit]
    return max(0, (value - r) / (a - r))


norm1 = [normalize(val, crit) for val, crit in zip(method1_values, criteria)]
norm2 = [normalize(val, crit) for val, crit in zip(method2_values, criteria)]
norm3 = [normalize(val, crit) for val, crit in zip(method3_values, criteria)]

angles = np.linspace(0, 2 * np.pi, len(criteria), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], criteria)

# Rysowanie krzywych
norm1 += norm1[:1]
norm2 += norm2[:1]
norm3 += norm3[:1]
ax.plot(angles, norm1, linewidth=8, label='Metoda punktu odniesienia')
ax.fill(angles, norm1, alpha=0.25)
# ax.plot(angles, norm2, linewidth=2, label='Metoda punktu odniesienia (niska beta)')
# ax.fill(angles, norm2, alpha=0.25)
ax.plot(angles, norm2, linewidth=2, label="Metoda oparta o logikę rozmytą")
ax.fill(angles, norm2, alpha=0.25)
ax.plot(angles, norm3, linewidth=2, label="Metoda Zimmermanna")
ax.fill(angles, norm3, alpha=0.25)

print(sum(norm1))
print(sum(norm2))
print(sum(norm3))
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.title('Porównanie rozwiązań — kryteria')
plt.show()
