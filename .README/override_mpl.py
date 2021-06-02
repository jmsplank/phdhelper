from phdhelper.helpers import override_mpl
from phdhelper.helpers.os_shortcuts import *
import matplotlib.pyplot as plt
import numpy as np

override_mpl.override()
plots_path = new_path(get_path(__file__))

x = np.arange(10)
y = np.sin(x) ** 2

x2 = np.linspace(0, 9, 100)
y2 = np.sin(x2) ** 3

plt.plot(x, y)
plt.plot(x2, y2)
plt.savefig(plots_path("new_default.png"))
plt.close()

override_mpl.override("book_gs")
plt.plot(x, y)
plt.plot(x2, y2)
plt.savefig(plots_path("book_style.png"))
