from dataclasses import dataclass
from typing import Protocol, Tuple, Union

import numpy as np
from scipy import stats

from src.transformations import add_lags, compute_adstock, compute_hill

ShapeObject = Union[int, Tuple[int]]


class Distribution(Protocol):
    """Protocol class defining distribution objects."""

    def rvs(self, size: ShapeObject,random_state: int = 123) -> np.ndarray:
        """Generates a sample from the underlying random variable distribution."""
        ...


class ScaledDistribution(Protocol):
    """Protocol class defining distibutions that get scaled"""

    def rvc(self, size: ShapeObject,random_state: int = 123) -> Tuple[np.ndarray, np.ndarray]:
        """Generates a sample from an underlying random variable distribution and scales the outputs"""
        ...


@dataclass
class Constant:
    c: float

    def rvs(self, size: ShapeObject = 1) -> np.ndarray:
        return np.ones(size) * self.c


@dataclass
class MarketingVar:
    """Generates a random variable transformed by adstock and hill."""

    variable: stats.distributions.rv_frozen
    l: stats.distributions.rv_frozen
    alpha: stats.distributions.rv_frozen
    d: stats.distributions.rv_frozen
    half_saturation: stats.distributions.rv_frozen
    slope: stats.distributions.rv_frozen

    def rvs(
        self,
        size: ShapeObject = 1,
        random_state: int = 123,
        return_metadata: bool = False,
    ) -> Tuple[np.ndarray, np.array]:
        """Generates a random sample of a marketing variable
        Args:
            size (ShapeObject, optional): size of the sample. Defaults to 1.
            random_state (int, optional): parameter passed to scipy random
            variables to control the random state. Defaults to None.
            return_metadata (bool, optional): flag on whether function returns
            the orignal sampled data and the transformation parameters. Defaults
            to False
        Returns:
            Tuple[np.ndarray, np.ndarray]: scaled data and non-scaled data
        """
        # sample parameters
        l = int(self.l.rvs(1, random_state))
        alpha = float(self.alpha.rvs(1, random_state))
        d = int(self.d.rvs(1, random_state))
        half_saturation = float(self.half_saturation.rvs(1, random_state))
        slope = float(self.slope.rvs(1, random_state))

        # sample data + burnin period
        sample = self.variable.rvs(
            size + 2 * l, random_state
        )  # TODO: make resilient to tuples

        # apply addstock
        adstock_sample = compute_adstock(add_lags(sample, l), d, alpha)
        # apply hill
        hill_sample = compute_hill(adstock_sample, half_saturation, slope)

        # remove burnin period
        sample = sample[2 * l :]
        hill_sample = hill_sample[2 * l :]

        if not return_metadata:
            return hill_sample, sample
        else:
            parameters = {
                "l": l,
                "alpha": alpha,
                "d": d,
                "half_saturation": half_saturation,
                "slope": slope,
            }

            return hill_sample, sample, parameters


class ControlVariable:
    """Generates a random variable scaled used a MinMaxScaler"""

    def __init__(self, variable: stats.distributions.rv_frozen) -> None:
        self.variable = variable

    def rvs(
        self, shape: ShapeObject, random_state: int = 123
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Generates a control variable and scales it using a MaxAbsScaler
        Args:
            shape (ShapeObject): shape of the output variable
            random_state (int, optional): parameter passed to scipy random
            variables to control the random state. Defaults to None.
        Returns:
            Tuple[np.ndarray, np.ndarray]: scaled data and non-scaled data
        """
        sample = self.variable.rvs(shape, random_state)  # sample initial variable
        max_abs_sample = np.max(np.abs(sample))  # recover max absolute value
        scaled_sample = sample / max_abs_sample  # scale sample

        return scaled_sample, sample
