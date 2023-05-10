"""Python implementation of Conway's game of life.

For more information, see:
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

Requirements:
  - numpy
  - matplotlib

Usage:
  - $python3 life <grid_size:int>

 """


import matplotlib as mlb
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import requests
import sys


def update(
    _, img: mlb.image.AxesImage, grid: np.ndarray, N: int
) -> mlb.image.AxesImage:
    # Avoid interim changes that affect the outcome
    new_grid = grid.copy()

    # Apply rules to all cells expect those on the margins
    for i in range(1, N - 1):
        for j in range(1, N - 1):
            alive_neighbors = int(
                np.sum(grid[i - 1 : i + 2, j - 1 : j + 2]) - grid[i][j]
            )  # Sum of the 8 cells surrounding it

            # 3 alive neighbors cause dead cells to become alive
            if not grid[i][j] and alive_neighbors == 3:
                new_grid[i][j] = 1

            # Alive cells with too many or too few neighbors die
            elif grid[i][j] and alive_neighbors not in (2, 3):
                new_grid[i][j] = 0

    img.set_data(grid)
    grid[:] = new_grid[:]
    return img


def main() -> None:
    N = int(sys.argv[1])

    target_url = "https://conwaylife.com/patterns/p256glidergunwithboatbits.cells"

    response = requests.get(target_url)
    data = response.text
    idx = data.find("..")
    new = data[idx:].split()
    cols = len(new[0])
    rows = len(new)

    binary = {".": 0, "O": 1}
    mat = np.zeros((rows, cols))
    for i, j in enumerate(new):
        mat[i] = [binary[k] for k in j]

    grid = mat
    N = mat.shape[0]
    # Generates the same random numbers for consistency
    np.random.seed(0)

    # Creates a matrix of size N-2xN-2 randomly filled with boolean values
    # grid = np.random.randint(2, size=(N - 2, N - 2))

    # Avoid IndexError by zero-padding
    grid = np.pad(grid, 1, mode="constant")

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation="nearest", cmap="Greys")
    _anim = FuncAnimation(
        fig,
        update,
        fargs=(
            img,
            grid,
            N,
        ),
        frames=10,
        interval=30,
        save_count=50,
    )

    plt.show()


if __name__ == "__main__":
    main()
