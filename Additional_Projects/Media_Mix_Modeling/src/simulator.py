from dataclasses import dataclass, field
from datetime import datetime

import numpy as np
from statsmodels.tsa.arima_process import arma_generate_sample

from src.parser import YamlParser


@dataclass
class Simulator:
    src_path: str
    """Path of Yaml config file"""
    size: int = field(default=104)
    """Number of time observations to generate"""
    baseline: np.ndarray = field(init=False)
    """Baseline level of sales"""
    seasonality: np.ndarray = field(init=False)
    """Combined seasonality effects"""
    media: np.ndarray = field(init=False)
    """Transformed media variables"""
    media_spends: np.ndarray = field(init=False)
    """Raw media variables"""
    control: np.ndarray = field(init=False)
    """Control variables"""
    noise: np.ndarray = field(init=False)
    """Unexplained effects"""
    random_state: int = 123

    def generate_data(self, parser) -> None:
        self._sample_distributions(parser)
        self._generate_seasonality()

        self.sales = (
            self.baseline[:, None]
            + self.seasonality[:, None]
            + self.media @ self.media_betas
            + self.control @ self.control_betas
            + self.noise[:, None]
        )
        self._generate_metadata()

    def _sample_distributions(self, parser: YamlParser):
        # unpack parser
        baseline_data, media_data, control_data, noise_dist = parser.parse_data()
        baseline_dist, baseline_coefs = baseline_data
        self.media_names, self.media_dists, media_coefs = media_data
        self.control_names, control_dists, control_coefs = control_data

        # generate samples
        self.baseline = baseline_dist.rvs(self.size)
        self.noise = noise_dist.rvs(self.size)
        #print(media_data[1])


        self.control = []
        self.control_spends = []
        for control_dist in control_dists:
            scaled_control, control_spends = control_dist.rvs(self.size)
            self.control.append(scaled_control),
            self.control_spends.append(control_spends)
        self.control = np.array(self.control).T
        self.control_spends = np.array(self.control_spends).T

        # generate media spends and transformed variables
        self.media = []
        self.media_parameters = []
        self.media_spends = []
        for media_dist in self.media_dists:
            transformed_media, media_spends, params = media_dist.rvs(
                self.size, return_metadata=True
            )
            self.media.append(transformed_media),
            self.media_spends.append(media_spends)
            self.media_parameters.append(params)
        self.media = np.array(self.media).T
        self.media_spends = np.array(self.media_spends).T

        # sample coefficients
        self.media_betas = np.array(
            [media_coef["beta"].rvs(1, random_state= 123) for media_coef in media_coefs]
        )
        self.control_betas = np.array(
            [control_coef["beta"].rvs(1, random_state= 123) for control_coef in control_coefs]
        )
        self.trimestral_seasonality = baseline_coefs["trimester_season"].rvs(1, random_state= 123)
        self.yearly_seasonality = baseline_coefs["year_season"].rvs(1, random_state= 123)
        self.arma_scale = baseline_coefs["arma_scale"].rvs(1, random_state= 123)
        self.trend_beta = baseline_coefs["trend_beta"].rvs(1, random_state= 123)

    def _generate_seasonality(self) -> None:
        year_season = self.yearly_seasonality * np.cos(
            np.arange(self.size) * 2 * np.pi / 52
        )
        monthly = self.trimestral_seasonality * np.cos(
            np.arange(self.size) * 2 * np.pi / 4
        )
        ma_noise = arma_generate_sample(
            ar=[1], ma=[1, 0.9, 0.5, 0.2, 0.1], nsample=self.size, scale=self.arma_scale
        )
        trend = self.trend_beta * np.arange(self.size)

        self.seasonality = year_season + monthly + ma_noise + trend

    def _generate_metadata(self) -> None:
        # auto-generates info and stores it in a dict
        self.metadata = {
            "timestamp": datetime.now().strftime("%H:%m:%S %d/%m/%Y"),
            "size": int(self.size),
            "media_names": self.media_names,
            "media_betas": [float(beta) for beta in self.media_betas],
            "media_parameters": self.media_parameters,
            "control_names": self.control_names,
            "control_betas": [float(beta) for beta in self.control_betas],
            "trimestral_seasonality": float(self.trimestral_seasonality),
            "yearly_seasonality": float(self.yearly_seasonality),
            "arma_scale": float(self.arma_scale),
            "trend_beta": float(self.trend_beta),
        }
