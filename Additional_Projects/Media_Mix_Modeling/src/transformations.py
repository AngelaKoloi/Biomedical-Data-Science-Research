from numbers import Number
from typing import Union

import numpy as np

Hyperparam = Union[Number, np.ndarray]


def compute_hill(
    spends: np.ndarray, half_saturation: Hyperparam, slope: Hyperparam
) -> np.ndarray:
    """Applies a Hill transformation to the marketing data.
    Args:
        spends (np.ndarray): array with marketing spends of shape n_obs x 1
        half_saturations (Hyperparam): half saturation parameter for each
        marketing channel
        slopes (Hyperparam): slope parameter for each marketing channel
    Raises:
        ValueError: if half saturation does not lie in the interval [0, 1]
        ValueError: if slope is negative
    Returns:
        np.ndarray: array with the transformed data

    Reference:
        https://en.wikipedia.org/wiki/Hill_equation_(biochemistry)
    """
    _validate_hill_parameters(spends, half_saturation, slope)
    return 1 / (1 + (spends / half_saturation) ** (-slope))


def compute_adstock(
    lagged_spends: np.ndarray, delay: float, alpha: float
) -> np.ndarray:
    """Implements a delayed geometric decay to lagged marketing spend
    observations. The input array must be shaped according to this pattern:

    n_observations x lags
    Args:
        lagged_spends (np.ndarray): array of shape n_observations x lags
        containing the lagged marketing observations
        delay (float): list with the delay parameters for each marketing
        channel.
        alpha (float): geometric decay parameter for each marketing channel
    Returns:
        np.ndarray: array of shape n_observations with the transformed variables
    """
    lag_weights = np.arange(lagged_spends.shape[1])
    lag_weights = np.power(alpha, (lag_weights - delay) ** 2)
    adstock_spends = np.dot(lagged_spends, lag_weights) / lag_weights.sum()

    return adstock_spends


def add_lags(array: np.ndarray, max_lag: int) -> np.ndarray:
    """Adds lagged versions of the original array to an additional dimension
    Args:
        array (np.ndarray): original array
        max_lag (int): number of lagged series to be added
    Raises:
        ValueError: when max_lag is lower than 0
        ValueError: when max_lag is larger than the size of the array
    Returns:
        np.ndarray: an array with the lagged observations
    """
    if max_lag < 0:
        raise ValueError("max_lag value must superior or equal 0")

    if max_lag > len(array):
        raise ValueError("max_lag value superior to nb of obs in array")

    # initialize output array
    lagged_array = np.zeros(array.shape + (max_lag,))

    for lag in range(max_lag):
        lagged_array[:, lag] = np.roll(array, lag)
        # erase carried observations carried over from the end of array
        lagged_array[:lag, lag] = 0

    return lagged_array


def compute_adstock_weights(
    lags: int, delay: float, alpha: float, n_steps: int = 100, x: np.ndarray = None
):
    """Function to compute adstock lag weights"""
    if x is None:
        lag_weights = np.arange(lags, step=(lags / n_steps))
    else:
        lag_weights = x

    return lag_weights, np.power(alpha, (lag_weights - delay) ** 2)


def _validate_hill_parameters(spends: np.ndarray, half_saturation, slope):
    if not isinstance(half_saturation, Number):  # manage 2D inputs
        if len(half_saturation.shape) != 2:
            raise ShapeError("Array of half saturations must be 2D")

        if (spends.shape[1] != half_saturation.shape[1]) and (
            spends.shape[0] != half_saturation.shape[0]
        ):
            raise ShapeError(
                "operands cannot be broadcast together with shapes "
                f"{spends.shape} {half_saturation.shape}"
            )

        if any((half_saturation < 0).flatten()) or any(
            (half_saturation > 1).flatten()
        ):  # validate support of parameter
            raise ValueError("half saturation value must be in [0,1]")
    else:
        if (half_saturation < 0) or (
            half_saturation > 1
        ):  # validate support of parameter
            raise ValueError("half saturation value must be in [0,1]")

    if not isinstance(slope, Number):  # manage 2D inputs
        if len(half_saturation.shape) != 2:
            raise ShapeError("Array of slope must be 2D")

        if (spends.shape[1] != slope.shape[1]) and (spends.shape[0] != slope.shape[0]):
            raise ShapeError(
                f"operands cannot be broadcast together with shapes "
                f"{spends.shape} {slope.shape}"
            )

        if any((slope < 0).flatten()):
            raise ValueError(
                "slope value must be greater than 0"
            )  # validate support of parameter
    else:
        if slope < 0:
            raise ValueError(
                "slope value must be greater than 0"
            )  # validate support of parameter


class ShapeError(Exception):
    pass
