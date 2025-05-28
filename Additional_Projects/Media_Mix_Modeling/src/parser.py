from typing import Dict, List, Tuple

import yaml
from scipy import stats

from src.distributions import Constant, ControlVariable, Distribution, MarketingVar


class YamlParser:
    """Parser used to read YAML config files used to generate MMM data."""

    def __init__(self, yaml_path) -> None:
        self.path = yaml_path
        self._read_yaml(yaml_path)

    def parse_data(self) -> Tuple[Distribution]:
        """Parses the data containied in the YAML config file.

        Returns:
        Tuple[Distribution]: tuple containg the distributions of the baseline,
        the media and control variables, and the noise.
        """
        # get baseline
        baseline_parsed_data = self._parse_baseline()
        # get media vars
        media_parsed_data = self._parse_marketing_vars()
        # get control vars
        control_parsed_data = self._parse_control_vars()
        # get noise
        noise_distribution = self._parse_distribution_data(self._noise_data)

        return (
            baseline_parsed_data,
            media_parsed_data,
            control_parsed_data,
            noise_distribution,
        )

    def _read_yaml(self, yaml_path):
        # reads config file
        with open(yaml_path, "r") as yaml_file:
            data = yaml.load_all(yaml_file, yaml.Loader)
            (
                self._baseline_data,
                self._media_data,
                self._control_data,
                self._noise_data,
            ) = list(data)

    def _parse_baseline(self):
        baseline_distribution = Constant(self._baseline_data["baseline"])
        baseline_coefficients = {
            var: self._parse_distribution_data(coef)
            for var, coef in self._baseline_data["coefficients"].items()
        }

        return baseline_distribution, baseline_coefficients

    def _parse_marketing_vars(self):
        names, variables, coefficients = self._parse_regressor_data(self._media_data)
        # initialize new output lists
        transformed_data = []
        regression_coefs = []
        for var, coefs in zip(variables, coefficients):
            # add beta to new coefficient list
            regression_coefs.append({"beta": coefs["beta"]})
            # remove beta from list of coefficients
            del coefs["beta"]
            # build random varaible with adstock and hill transformations
            transformed_data.append(MarketingVar(var, **coefs))

        return names, transformed_data, regression_coefs

    def _parse_control_vars(self):
        names, variables, coefficients = self._parse_regressor_data(self._control_data)
        # initialize new output lists
        scaled_data = []
        regression_coefs = []
        for var, coefs in zip(variables, coefficients):
            # add beta to new coefficient list
            regression_coefs.append({"beta": coefs["beta"]})
            # remove beta from list of coefficients
            del coefs["beta"]
            # build random varaible with adstock and hill transformations
            scaled_data.append(ControlVariable(var, **coefs))
        print(regression_coefs)

        return names, scaled_data, regression_coefs

    def _parse_regressor_data(
        self, data: dict
    ) -> Tuple[
        List[Distribution], List[Dict[str, Distribution]],
    ]:
        # parses data from marketing and control variables
        # initialize output lists
        names = []
        distributions = []
        coef_distributions = []
        for var, var_data in data.items():
            names.append(var_data["name"])
            # get distribution of regressor
            distributions.append(
                self._parse_distribution_data(var_data["distribution"])
            )
            # get distribution of regressor's coefficients
            coef_distributions.append(
                {
                    coef: self._parse_distribution_data(coef_dist)
                    for coef, coef_dist in var_data["coefficients"].items()
                }
            )

        return names, distributions, coef_distributions

    def _parse_distribution_data(
        self, distribution_data: dict
    ) -> stats.distributions.rv_frozen:
        # looks up for scipy.stats distribution and initializes it with the given parameters
        distribution = getattr(stats, distribution_data["distribution"])
        return distribution(**distribution_data["parameters"])
