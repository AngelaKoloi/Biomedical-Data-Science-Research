import json
import os
from dataclasses import dataclass, field
from shutil import copy
from typing import Dict

import numpy as np

SALES_FILE_NAME = "mmm_sales.npy"
MEDIA_FILE_NAME = "mmm_media.npy"
MEDIA_SPENDS_FILE_NAME = "mmm_media_spends.npy"
CONTROL_FILE_NAME = "mmm_control.npy"
CONTROL_SPENDS_FILE_NAME = "mmm_control_spends.npy"
SEASONALITY_FILE_NAME = "mmm_seasonality.npy"
CONFIG_YAML_FILE_NAME = "config_copy.yaml"
METADATA_FILE_NAME = "metadata.json"


def save_generated_data_to_folder(
    out_folder: str,
    input_path: os.PathLike,
    sales: np.ndarray,
    media: np.ndarray,
    media_spends: np.ndarray,
    control: np.ndarray,
    control_spends: np.ndarray,
    seasonality: np.ndarray,
    metadata: dict,
):
    # save relevant numpy arrays
    np.save(os.path.join(out_folder, SALES_FILE_NAME), sales)
    np.save(os.path.join(out_folder, MEDIA_FILE_NAME), media)
    np.save(os.path.join(out_folder, MEDIA_SPENDS_FILE_NAME), media_spends)
    np.save(os.path.join(out_folder, CONTROL_FILE_NAME), control)
    np.save(os.path.join(out_folder, CONTROL_SPENDS_FILE_NAME), control_spends)
    np.save(os.path.join(out_folder, SEASONALITY_FILE_NAME), seasonality)
    # copy config file to output folder
    copy(input_path, os.path.join(out_folder, CONFIG_YAML_FILE_NAME))
    # save metadate to json file
    with open(os.path.join(out_folder, METADATA_FILE_NAME), "w") as metadata_file:
        json.dump(metadata, metadata_file)


@dataclass
class SimulatedDataLoader:
    data_path: str
    _control_scaled: np.ndarray = field(default=None, init=False)
    _control_spends: np.ndarray = field(default=None, init=False)
    _media_transformed: np.ndarray = field(default=None, init=False)
    _media_spends: np.ndarray = field(default=None, init=False)
    _sales: np.ndarray = field(default=None, init=False)
    _seasonality: np.ndarray = field(default=None, init=False)
    _metadata: Dict = field(default=None, init=False)

    def __post_init__(self):
        self.config_path = os.path.join(self.data_path, CONFIG_YAML_FILE_NAME)

    @property
    def control_scaled(self):
        if not self._control_scaled:
            return np.load(os.path.join(self.data_path, CONTROL_FILE_NAME))
        else:
            return self._control_scaled

    @property
    def control_spends(self):
        if not self._control_spends:
            return np.load(os.path.join(self.data_path, CONTROL_SPENDS_FILE_NAME))
        else:
            return self._control_spends

    @property
    def media_transformed(self):
        if not self._media_transformed:
            return np.load(os.path.join(self.data_path, MEDIA_FILE_NAME))
        else:
            return self._media_transformed

    @property
    def media_spends(self):
        if not self._media_spends:
            return np.load(os.path.join(self.data_path, MEDIA_SPENDS_FILE_NAME))
        else:
            return self._media_spends

    @property
    def sales(self):
        if not self._sales:
            return np.load(os.path.join(self.data_path, SALES_FILE_NAME))
        else:
            return self._sales

    @property
    def seasonality(self):
        if not self._seasonality:
            return np.load(os.path.join(self.data_path, SEASONALITY_FILE_NAME))
        else:
            return self._seasonality

    @property
    def metadata(self):
        if not self._metadata:
            with open(
                os.path.join(self.data_path, METADATA_FILE_NAME), "r"
            ) as metadata_file:
                return json.load(metadata_file)
        else:
            return self._metadata

    @property
    def media_betas(self):
        return np.array(self.metadata["media_betas"])[:, None]

    @property
    def media_names(self):
        return np.array(self.metadata["media_names"])

    @property
    def control_betas(self):
        return np.array(self.metadata["control_betas"])[:, None]

    @property
    def control_names(self):
        return np.array(self.metadata["control_names"])

    @property
    def media_lags(self):
        return self._recover_media_parameter("l")

    @property
    def media_alphas(self):
        return self._recover_media_parameter("alpha")

    @property

    def media_delays(self):
        return self._recover_media_parameter("d")

    @property
    def media_half_saturations(self):
        return self._recover_media_parameter("half_saturation")

    @property
    def media_slopes(self):
        return self._recover_media_parameter("slope")

    def _recover_media_parameter(self, param_name):
        output = []
        for media_parameters in self.metadata["media_parameters"]:
            output.append(media_parameters[param_name])

        return np.array(output)[:, None]
