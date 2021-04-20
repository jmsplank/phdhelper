import numpy as np
import pyspedas
from phdhelper.helpers import title_print
from phdhelper.helpers.CONSTANTS import c, k_B, m_e, m_i, mu_0, q
from pytplot import data_quants
import matplotlib.pyplot as plt
from datetime import datetime as dt
from cached_property import cached_property


class EventHandler:
    FPI = None
    FPI_DIST = None
    FSM = None
    FGM = None

    trange = None
    probe = None

    def load_FGM(self):
        self.FGM = pyspedas.mms.fgm(
            trange=self.trange, probe=self.probe, data_rate="brst"
        )

    def load_FSM(self):
        raise NotImplementedError()

    def load_FPI_DIST(self):
        self.FPI_DIST = pyspedas.mms.fpi(
            trange=self.trange,
            probe=self.probe,
            data_rate="brst",
            datatype="dis-dist",
        )

    def load_FPI(self):
        self.FPI = pyspedas.mms.fpi(
            trange=self.trange, probe=self.probe, data_rate="brst"
        )

    @staticmethod
    def get_tplot_data(var_str, sl=None, time=False):
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


class TimeMMS(EventHandler):
    def __init__(self, kw):
        self.kw = kw

    @cached_property
    def timestamp(self):
        return self.get_tplot_data(self.kw, time=True)

    @cached_property
    def date_time(self):
        return np.array([dt.utcfromtimestamp(t) for t in self.timestamp])

    def date_string(self, fmt="%H:%M"):
        return np.array([dt.strftime(t, fmt) for t in self.date_time])


class Species(EventHandler):
    def __init__(self, kw) -> None:
        self.kw = kw

    @cached_property
    def value(self):
        return self.get_tplot_data(self.kw)

    @cached_property
    def time(self):
        return TimeMMS(self.kw)

    def plot(self):
        plt.plot(self.value)

    def __repr__(self):
        return (
            f"Species({self.kw})"
            "Available properties:"
            "   value"
            "Available methods:"
            "   plot"
        )


class MultiSpecies:
    def __init__(self, ion_kw: str, electron_kw: str) -> None:
        self.ion_kw = ion_kw
        self.electron_kw = electron_kw

    @cached_property
    def ion(self):
        return Species(self.ion_kw)

    @cached_property
    def electron(self):
        return Species(self.electron_kw)


class Event(EventHandler):
    def __init__(
        self, trange: str, required_instruments: str, probe: str = "1"
    ) -> None:
        self.trange = trange
        self.required_instruments = required_instruments.upper()
        self.probe = probe

        if "FGM" in required_instruments:
            self.load_FGM()
        if "FPI" in required_instruments:
            self.load_FPI()
        if "FSM" in required_instruments:
            self.load_FSM()
        if "FPI_DIST" in required_instruments:
            self.load_FPI_DIST()

    @cached_property
    def B(self):
        return Species(f"mms{self.probe}_fgm_b_gse_brst_l2")

    @cached_property
    def v(self):
        return MultiSpecies(
            f"mms{self.probe}_dis_bulkv_gse_brst",
            f"mms{self.probe}_des_bulkv_gse_brst",
        )

    @cached_property
    def T(self):
        return MultiSpecies(
            f"mms{self.probe}_dis_temppara_brst",
            f"mms{self.probe}_dis_tempperp_brst",
        )

    @cached_property
    def E(self):
        return MultiSpecies(
            f"mms{self.probe}_dis_energyspectr_omni_brst",
            f"mms{self.probe}_des_energyspectr_omni_brst",
        )

    # @property
    # def v_0(self, species="i"):
    #     title_print("Calculating background flow speed")
    #     species = self.Species(species)
    #     if species.ion:
    #         self.v_0_i = np.mean(np.linalg.norm(self.v_i, axis=1))
    #     if species.elec:
    #         self.v_0_e = np.mean(np.linalg.norm(self.v_e, axis=1))

    # @property
    # def v_A(self):
    #     title_print("Calculating Alfven speed")
    #     self.v_A = self.mean_B / np.sqrt(mu_0 * self.number_density_i) / 1e3

    # @property
    # def number_density(self, species="i"):
    #     species = self.Species(species)
    #     if species.ion:
    #         self.number_density_i = (
    #             self.get_tplot_data(f"mms{self.probe}_dis_numberdensity_brst") * 1e6
    #         ).mean()
    #     if species.elec:
    #         self.number_density_e = (
    #             self.get_tplot_data(f"mms{self.probe}_des_numberdensity_brst") * 1e6
    #         ).mean()

    # @property
    # def beta(self, species="i"):
    #     title_print("Calculating plasma betas")
    #     species = self.Species(species)
    #     magPress = self.mean_B ** 2 / (2 * mu_0)
    #     if species.ion:
    #         self.beta_i = (
    #             self.number_density_i * k_B * self.T_i[:, 0].mean()
    #         ) / magPress
    #     if species.elec:
    #         self.beta_e = (
    #             self.number_density_e * k_B * self.T_e[:, 0].mean()
    #         ) / magPress

    # @property
    # def rho(self, species="i"):
    #     title_print("Calculating gyroradius")
    #     species = self.Species(species)
    #     if species.ion:
    #         i_thermal_velocity = np.sqrt(self.T_i[:, 1].mean() * 2 * q / m_i) / 1e3
    #         i_gyrofrequency = q * self.mean_B / m_i
    #         self.rho_i = i_thermal_velocity / i_gyrofrequency
    #     if species.elec:
    #         e_thermal_velocity = np.sqrt(self.T_i[:, 1].mean() * 2 * q / m_e) / 1e3
    #         e_gyrofrequency = q * self.mean_B / m_e
    #         self.rho_e = e_thermal_velocity / e_gyrofrequency

    # @property
    # def p(self, species="i"):
    #     title_print("Calculating Intertial length")
    #     species = self.Species(species)
    #     if species.ion:
    #         i_plasma_frequency = 1.32e3 * np.sqrt(self.number_density_i)
    #         self.p_i = c / i_plasma_frequency
    #         self.p_i /= 1e3
    #     if species.elec:
    #         e_plasma_frequency = 5.64e4 * np.sqrt(self.number_density_e)
    #         self.p_e = c / e_plasma_frequency
    #         self.p_e /= 1e3

    # @property
    # def time(self, var="B"):
    #     title_print("Getting time arrays")
    #     var = var.split("|")
    #     if "B" in var:
    #         self.time_B = self.get_tplot_data(
    #             f"mms{self.probe}_fgm_b_gse_brst_l2", time=True
    #         )
    #     if "V" in var:
    #         self.time_V = self.get_tplot_data(
    #             f"mms{self.probe}_dis_bulkv_gse_brst", time=True
    #         )
    #     if "e" in var:
    #         self.time_e = self.get_tplot_data(
    #             f"mms{self.probe}_des_temppara_brst", time=True
    #         )