import numpy as np
import matplotlib.pyplot as plt
from phdhelper.helpers import override_mpl, os_shortcuts

save_fig = os_shortcuts.new_path(os_shortcuts.get_path(__file__))

override_mpl.override()
override_mpl.cmaps("custom_diverging")

x, y = np.mgrid[0:12:1000j, 0:12:1000j]
z = np.sin(x) ** 3 + np.sin(y) ** 3

fig, ax = plt.subplots(2, 1, sharex=True, sharey=True)

im1 = ax[0].pcolormesh(x, y, z, shading="nearest")
fig.colorbar(im1, ax=ax[0])
im2 = ax[1].pcolormesh(
    x,
    y,
    z,
    cmap="custom_diverging",
    shading="nearest",
)
fig.colorbar(im2, ax=ax[1])
plt.tight_layout()
plt.savefig(save_fig("default_cmaps.png"))
plt.close()

override_mpl.override("book_gs")
plt.pcolormesh(x, y, z, shading="nearest")
plt.colorbar()
plt.tight_layout()
plt.savefig(save_fig("book_cmap.png"))
