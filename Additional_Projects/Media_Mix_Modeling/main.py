import argparse
import os
import warnings
from datetime import datetime

from src.parser import YamlParser
from src.simulator import Simulator
from src.utils import save_generated_data_to_folder

formated_date = datetime.now().strftime("%Y-%m-%d-%H-%M")
OUTPUT_FOLDER = f"simulated_data/{formated_date}"

arg_parser = argparse.ArgumentParser(
    prog="MMM data generator",
    description="Program to generate artificial marketing spending data",
)
arg_parser.add_argument("-f", "--file", required=True, help="YAML config file")
arg_parser.add_argument("-s", "--size", default=104, help="Size of output data")
arg_parser.add_argument(
    "-o", "--out", default=OUTPUT_FOLDER, help="Name of the output folder"
)


def main(file, size, output_folder):
    # make output file name & create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        warnings.warn(f"Overwriting data in {output_folder}")

    # parse config file
    parser = YamlParser(file)
    # simulate data
    simulator = Simulator(src_path=file, size=size)

    simulator.generate_data(parser)
    save_generated_data_to_folder(
        out_folder=output_folder,
        input_path=parser.path,
        sales=simulator.sales,
        media=simulator.media,
        media_spends=simulator.media_spends,
        control=simulator.control,
        control_spends=simulator.control_spends,
        seasonality=simulator.seasonality,
        metadata=simulator.metadata,
    )


if __name__ == "__main__":
    args = arg_parser.parse_args()
    main(args.file, int(args.size), args.out)
