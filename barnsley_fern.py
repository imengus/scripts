# Recreates the Barnsley's fern fractal

import matplotlib.pyplot as plt
import numpy as np

def f(coeffs, choice, u):
    coeff = coeffs[choice] # 0 = f1, 1 = f2, 2 = f3, 3 = f4
    a, b, c, d, e, f = coeff
    mat = np.array([[a, b], [c, d]])
    vect = np.array([e, f])
    return mat @ u + vect # u_n+1

COEFFS = np.array([
    [0, 0, 0, 0.16, 0, 0], # f1
    [0.85, 0.04, -0.04, 0.85, 0, 1.60], # f2
    [0.20, -0.26, 0.23, 0.22, 0, 1.60], # f3
    [-0.15, 0.28, 0.26, 0.24, 0, 0.44] # f4
    ])
PROBS = np.array([0.01, 0.85, 0.07, 0.07]) # prob of finding u_n+1 via f1, f2, f3, or f4
ITERNUM = 100000


def main():
    u = np.zeros((2, ITERNUM)) # cols: vector u_n, rows: x and y
    for n in range(ITERNUM - 1):
        choice = np.random.choice([0, 1, 2, 3], p=PROBS)
        u[:, n+1] = f(COEFFS, choice, u[:, n])
    plt.scatter(u[0], u[1], color='0', s=1, alpha=0.1)
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()