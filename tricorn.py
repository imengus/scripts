import matplotlib.pyplot as plt
import numpy as np
from numba import njit

@njit
def create_matrix(size=1000):

    def pixel_color(Px, Py, mult, sub, coeff=-1):
        x0 = mult * Px - sub * 2.5
        y0 = mult * Py - sub
        x = y = it = 0
        max_iter = 20
        while (x**2 + y**2) <= 4 and it < max_iter:
            xtemp = x**2 - y**2 + x0
            y = coeff * 2*x*y + y0
            x = xtemp
            it += 1
        return it / max_iter
    
    mult = 1.5 / size
    sub = 1.5 / 2
    mat = np.zeros((size, size), dtype=np.float32)
    for Px in range(size):
        for Py in range(size):
            mat[Py, Px] = pixel_color(Px, Py, mult, sub)
    return mat

def plot_matrix():
    mat = create_matrix(size=35000)
    plt.imshow(mat, cmap="hot_r")
    plt.axis('off')
    # plt.gca().set_aspect('equal')
    plt.show()


def main():
    plot_matrix()

if __name__ == "__main__":
    main()