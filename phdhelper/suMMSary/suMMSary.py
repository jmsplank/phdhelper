import numpy as np
import pyspedas
from phdhelper.helpers import title_print
from phdhelper.helpers.CONSTANTS import c, k_B, m_e, m_i, mu_0, q
from pytplot import data_quants


class EventSummary:
    fgm = None
    fpi = None
    fpi_dist = None

    def __init__(self, trange, probe):
        self.trange = trange
        self.probe = probe

        title_print("Getting time arrays")
        self.time_B = self.get_tplot_data(f"mms{probe}_fgm_b_gse_brst_l2", time=True)
        self.time_V = self.get_tplot_data(f"mms{probe}_dis_bulkv_gse_brst", time=True)
        self.time_E = self.get_tplot_data(f"mms{probe}_dis_dist_brst", time=True)

        title_print("Getting B field")
        self.B = self.get_tplot_data(f"mms{probe}_fgm_b_gse_brst_l2")

        title_print("Getting ion velocity")
        self.v_i = self.get_tplot_data(f"mms{probe}_dis_bulkv_gse_brst")

        title_print("Getting Ion energy")
        self.E_i = self.get_tplot_data(f"mms{probe}_dis_dist_brst")
        self.E_i = self.E_i.mean(axis=2)
        self.E_i = self.E_i.mean(axis=1)

        title_print("Calculating background flow speed")
        self.v_0 = np.mean(np.linalg.norm(self.v_i, axis=1))

        title_print("Calculating Alfven speed")
        self.i_number_density = (
            self.get_tplot_data(f"mms{probe}_dis_numberdensity_brst") * 1e6
        ).mean()  # convert from cm^-3
        self.mean_B = self.B[:, 3].mean() * 1e-9  # Convert from nT
        self.v_A = self.mean_B / np.sqrt(mu_0 * self.i_number_density) / 1e3

        title_print("Calculating plasma betas")
        magPress = self.mean_B ** 2 / (2 * mu_0)
        self.temp_para = (
            self.get_tplot_data(f"mms{probe}_dis_temppara_brst").mean() * q
        )  # Temp in eV
        # Ion
        self.beta_i = (self.i_number_density * k_B * self.temp_para) / magPress
        # Electron
        self.e_number_density = (
            self.get_tplot_data(f"mms{probe}_des_numberdensity_brst") * 1e6
        ).mean()
        self.beta_e = (self.e_number_density * k_B * self.temp_para) / magPress

        title_print("Calculating gyroradius")
        # Gyroradius
        self.temp_perp = self.get_tplot_data(f"mms{probe}_dis_tempperp_brst").mean()
        # Ion
        i_thermal_velocity = np.sqrt(self.temp_perp * 2 * q / m_i) / 1e3
        i_gyrofrequency = q * self.mean_B / m_i
        self.rho_i = i_thermal_velocity / i_gyrofrequency
        # Electron
        e_thermal_velocity = np.sqrt(self.temp_perp * 2 * q / m_e) / 1e3
        e_gyrofrequency = q * self.mean_B / m_e
        self.rho_e = e_thermal_velocity / e_gyrofrequency

        title_print("Calculating Intertial length")
        # Inertial Length
        # Ion
        i_plasma_frequency = 1.32e3 * np.sqrt(self.i_number_density)
        self.p_i = c / i_plasma_frequency
        self.p_i /= 1e3
        # Electron
        e_plasma_frequency = 5.64e4 * np.sqrt(self.e_number_density)
        self.p_e = c / e_plasma_frequency
        self.p_e /= 1e3

    def get_tplot_data(self, var_str, sl=None, time=False):
        if "fgm" in var_str:
            # Data is from fluxgate magnetometer
            # Check fgm data has been loaded
            if self.fgm is None:
                self.fgm = pyspedas.mms.fgm(
                    trange=self.trange, probe=self.probe, data_rate="brst"
                )
        elif "dist" in var_str:
            # Data is from fpi distributions
            # Check if fpi distributions are loaded
            if self.fpi_dist is None:
                self.fpi_dist = pyspedas.mms.fpi(
                    trange=self.trange,
                    probe=self.probe,
                    data_rate="brst",
                    datatype="dis-dist",
                )
        else:
            # Data is from FPI moments
            # Check moments are loaded
            if self.fpi is None:
                self.fpi = pyspedas.mms.fpi(
                    trange=self.trange, probe=self.probe, data_rate="brst"
                )

        if not time:
            if sl is None:
                # Get all data
                return data_quants[var_str].values
            else:
                return data_quants[var_str].values[sl]
        else:
            if sl is None:
                # Get all data
                return data_quants[var_str].coords["time"].values
            else:
                return data_quants[var_str].coords["time"].values[sl]

    @staticmethod
    def _2dp(num):
        return f"{num:.2e}"

    def __str__(self):
        return f"""
==================================
EventSummary: 
    trange -> {self.trange}
    probe  -> {self.probe}
----------------------------------

Time Arrays:
    time_B -> len {len(self.time_B)}
    time_V -> len {len(self.time_V)}
    time_E -> len {len(self.time_E)}

Parameters:
    mean B -> {self._2dp(self.mean_B * 1e9)}nT
    Background flow speed -> {self._2dp(self.v_0)}km/s
    Alfven speed -> {self._2dp(self.v_A)}km/s
    Plasma beta (ion) -> {self._2dp(self.beta_i)}
    Plasma beta (e) -> {self._2dp(self.beta_e)}
    Gyroradios (ion) -> {self._2dp(self.rho_i)}km
    Gyroradios (e) -> {self._2dp(self.rho_e)}km
    Inertial length (ion) -> {self._2dp(self.p_i)}km
    Inertial length (ion) -> {self._2dp(self.p_e)}km
==================================
"""
