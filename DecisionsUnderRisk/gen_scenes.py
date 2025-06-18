import numpy as np


def generate_scenarios(n_scenarios=10, df=5):
    mu = np.array([116, 102, 113, 100, 107, 110])
    Sigma = np.array([
        [36, 1, 0, 1, 1, 1],
        [1, 36, -1, -1, -3, -5],
        [0, -1, 49, 2, 2, 0],
        [1, -1, 2, 81, -5, -2],
        [1, -3, 2, -5, 64, -2],
        [1, -5, 0, -2, -2, 25]
    ])

    t_samples = np.random.standard_t(df, size=(n_scenarios, 6))

    L = np.linalg.cholesky(Sigma)
    correlated_samples = mu + (t_samples @ L.T) / np.sqrt(df / (df - 2))

    constrained_samples = np.clip(correlated_samples, 60, 140)

    ampl_format = "param price :=\n"
    for i in range(n_scenarios):
        scenario = f"S{i+1}"
        for j, (oil, month) in enumerate([("A", "Jan"), ("A", "Feb"), ("B", "Jan"), ("B", "Feb"), ("C", "Jan"), ("C", "Feb")]):
            ampl_format += f"    {oil} {month} {scenario} {int(constrained_samples[i, j])}\n"
    ampl_format += ";\n\n"

    ampl_format += "param p :=\n"
    for i in range(n_scenarios):
        ampl_format += f"    S{i+1} {1/n_scenarios}\n"
    ampl_format += ";"
    ampl_format += "\nset SCENARIOS :="
    for i in range(n_scenarios):
        ampl_format += f" S{i+1}"
    ampl_format += ";"
    return ampl_format


scenarios_ampl = generate_scenarios(100)

with open("scenarios2.dat", "w") as file:
    file.write(scenarios_ampl)

print(scenarios_ampl)
