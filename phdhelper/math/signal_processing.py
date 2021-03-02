import numpy as np
from tqdm import tqdm
from numba import njit, prange

from phdhelper.exceptions.phdException import OutOfBoundsException


def autocorrelate(x: np.ndarray, steps=None) -> np.ndarray:
    """Calculate the autocorrelation of a 1d signal
    http://en.wikipedia.org/wiki/Autocorrelation#Estimation
    """

    if len(x) == 0:
        return x
    if type(x) != np.array:
        x = np.array(x, dtype=float)
    x.astype(np.float64, copy=False)

    if steps is None:
        steps = len(x)
    else:
        if steps > len(x) - 1:
            raise OutOfBoundsException(
                steps, len(x) - 1, additional="Greater than len(x) - 1."
            )

    mean: float = np.mean(x)
    n: int = len(x)
    var: float = np.std(x) ** 2
    print(mean, n, var)
    x -= mean

    R = _acorr(x, steps, var, n)
    return R


@njit(parallel=True)
def _acorr(x, steps, var, n):
    R = np.empty(steps, np.float64)
    R[0] = 1.0
    for i in prange(1, steps):
        const: float = 1.0 / ((n - i) * var)
        xl = x[:-i]
        xr = x[i:]
        s = np.sum(xl * xr)

        R[i] = s * const

    return R


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    a = np.random.random(1000)
    r = autocorrelate(a)

    # x = np.linspace(0, 30 * np.pi, 1500)
    # a = np.sin(2 * np.pi * 0.1 * x) * np.sin(2 * np.pi * 0.11 * (x))
    # r = autocorrelate(a)

    # beating = {"input": a, "output": r}
    # np.save("phdhelper/tests/math/autocorrelate_beating.npy", beating)

    # data = np.load("phdhelper/tests/math/autocorrelate_beating.npy", allow_pickle=True)
    # a = data.item().get("input")
    # r = data.item().get("output")

    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(a)
    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(r)
    # ax2.plot(autocorrelate(a))
    plt.show()
