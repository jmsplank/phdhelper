import numpy as np
from typing import Literal


def lengths(
    s: Literal["i", "e"],
    out: Literal["rho", "d"] = "d",
    all=False,
    number_density=None,
    temp_perp=None,
    B_field=None,
    elementwise=False,
):
    """Plasma lengths.
    https://en.wikipedia.org/wiki/Plasma_parameters#Fundamental_plasma_parameters

    IN:
        s: Species
        number_density: for 'd' ONLY
        temp_perp: for 'rho' ONLY
        B_field: for 'rho' ONLY
        all: Return all as [rho, d]
        out: choose product to return, either 'd' OR 'rho'
    OUT:
        if all:
            [rho, d]
        if out == 'rho':
            rho
        if out == 'd':
            d
    """
    if (all) or (out == "d"):
        if not elementwise:
            n = number_density.mean()
        else:
            n = number_density
        const = 1.32e3 if s == "i" else 5.64e4
        omega_p = const * np.sqrt(n)
        d = 2.99792458e8 / omega_p
        d /= 1e3  # Inertial Length

    if all or out == "rho":
        T = temp_perp
        v = (
            np.sqrt(
                np.mean(T)
                * 2
                * 1.60217662e-19
                / (1.6726219e-27 if s == "i" else 9.10938356e-31)
            )
            / 1e3
        )
        B_scaled = B_field.copy() * 1e-9
        BT = np.linalg.norm(B_scaled, axis=1).mean()
        omega_c = 1.60217662e-19 * BT / (1.6726219e-27 if s == "i" else 9.10938356e-31)
        rho = v / omega_c  # Gyroradius

    if all:
        return np.array([rho, d])

    if out == "rho":
        return rho
    if out == "d":
        return d
