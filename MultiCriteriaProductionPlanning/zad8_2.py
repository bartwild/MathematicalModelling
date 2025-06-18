import matplotlib.pyplot as plt
zysk = [(120, 0), (130, 0), (150, 1), (170, 1)]
emisja = [(20, 1), (30, 1), (35, 0), (40, 0)]
koszt = [(30, 1), (70, 1), (80, 0), (90, 0)]
s1 = [(60, 1), (100, 1), (110, 0), (120, 0)]
s2 = [(40, 1), (50, 1), (55, 0), (60, 0)]
case1 = {
    "Zysk": (156.26, 1.0),
    "Emisja": (22.43, 1.0),
    "Koszt": (31.30, 1.0),
    "S1": (70,     1.0),
    "S2": (48,     1.0)
}
case2 = {
    "Zysk": (150, 1.0),
    "Emisja": (22.10526, 1.0),
    "Koszt": (30.31579, 1.0),
    "S1": (67.0526,    1.0),
    "S2": (48.1053,    1.0)
}
def plot_fn(ax, data, point, label, xlabel, color='blue'):
    xs, ys = zip(*data)
    ax.plot(xs, ys, color=color)
    ax.set_ylim(-0.05, 1.05)
    ax.set_title(label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("μ(x)")
fig, axs = plt.subplots(5, 1, figsize=(8, 15))
plot_fn(axs[0], zysk, None, "Funkcja przynależności - Zysk", "C")
plot_fn(axs[1], emisja, None, "Funkcja przynależności - Emisja", "Z")
plot_fn(axs[2], koszt, None, "Funkcja przynależności - Koszt", "K")
plot_fn(axs[3], s1, None, "Funkcja przynależności - Zużycie S1", "S1")
plot_fn(axs[4], s2, None, "Funkcja przynależności - Zużycie S2", "S2")

colors = {'case1': 'brown', 'case2': 'green'}
labels = {'case1': 'Metoda punktu ref.', 'case2': 'Metoda Zimmermanna'}
i = 2
for case, props in zip([case1, case2], ['case1', 'case2']):
    for ax, crit, data_fn in zip(axs, ["Zysk", "Emisja", "Koszt", "S1", "S2"], [zysk, emisja, koszt, s1, s2]):
        x, mu = case[crit]
        ax.scatter(x, mu, color=colors[props], label=labels[props])
        ax.annotate(f"{labels[props]}\n({x:.2f}, {mu:.2f})", (x, mu),
                    textcoords="offset points", xytext=(5, -10*i), ha='left', color=colors[props])
    i *= 2
axs[0].legend(loc='lower right')
plt.tight_layout()
plt.show()
