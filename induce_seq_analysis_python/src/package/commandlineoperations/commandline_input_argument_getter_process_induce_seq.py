"""
A collection of classes or functions that grabs commandline arguments
"""

__name__ = "__main__"

import argparse
import os

from package.fileoperations.filehandlers import globally_get_all_files, read_csv


class CliInputArgumentGetter:
    """Wrapper for argparse that returns an object of the class for ease of use"""

    @classmethod
    def get_cli_input_arguments(cls, args=None) -> argparse.Namespace:
        """gets input arguments from the commandline interface """

        parser = argparse.ArgumentParser(prog="process_induce_seq.py", usage="""process_induce_seq.py -h""",
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=("""
                    This script:
                        1. Filter out reads that have a mapping quality of < 30
                        2. Intersect each sample break bed file with the AsiSI site bed file
                        3. Sum and normalise the counts
                        4. Collect normalised number of AsiSI breaks
                        5. Plot the results: determine which samples are most likely to represent the control & treated 
                        subsets.

                    Required:
                        - Python >= 3.10
                        - python-dotenv>=1.0.0
                        - for additional dependencies, see requirements.txt

                """), )
        parser.add_argument("-o", "--path2out", help="absolute directory path to processed output files ",
                            required=True, )
        parser.add_argument("-i", "--path2breaks", help="absolute directory breaks bed file ", required=True, )
        parser.add_argument("-a", "--path2asisi", help="absolute file path to AsiSI sites bed file ", required=True, )
        parser.add_argument("-b", "--bed_extension", help="bed file extension", default="bed")
        parser.add_argument("-q", "--score_threshold", help="mapping quality score threshold", type=int, default=30)
        parser.add_argument("-s", "--sample_id", help="sample identifier", type=str, required=True)

        return parser.parse_args(args)

    @classmethod
    def check_input_arguments(cls, cli_input_arguments: argparse.Namespace) -> None:
        """ check or verify input arguments """

        if not os.path.exists(cli_input_arguments.path2breaks) and not os.path.isfile(cli_input_arguments.path2breaks):
            breaks_path_error_message = "breaks bed file {} does not exist!"
            raise FileNotFoundError(breaks_path_error_message.format(cli_input_arguments.path2breaks))

        if not os.path.exists(cli_input_arguments.path2out):
            path_out_error_message = "output directory {} does not exist!"
            raise FileNotFoundError(path_out_error_message.format(cli_input_arguments.path2out))

        if not os.path.exists(cli_input_arguments.path2asisi) and os.path.isfile(cli_input_arguments.path2asisi):
            asisi_path_error_message = "asisi bed file {} does not exist!"
            raise FileNotFoundError(asisi_path_error_message.format(cli_input_arguments.path2asisi))

        CliInputArgumentGetter.__check_bed_files(cli_input_arguments)

    @classmethod
    def __check_bed_files(cls, cli_input_arguments: argparse.Namespace) -> None:
        """ check if bam files """

        breaks_files: str = cli_input_arguments.path2breaks
        asisi_file: str = cli_input_arguments.path2asisi

        CliInputArgumentGetter.__iterate_through_bam_bed_files(breaks_files, asisi_file)

    @classmethod
    def __iterate_through_bam_bed_files(cls, breaks_bed_file: str, asisi_file: str) -> None:
        """ iterate through bam and bed files to process each bam and bed files individually """

        CliInputArgumentGetter.__check_bed_file(breaks_bed_file, "break file")

        CliInputArgumentGetter.__check_bed_file(asisi_file, "asisi file")

    @classmethod
    def __check_bed_file(cls, bed_file: str, file_type: str) -> None:
        """ check or verify input arguments """

        if not os.path.exists(bed_file):
            bed_file_path_error_message = "{} {} does not exist!"
            raise FileNotFoundError(bed_file_path_error_message.format(file_type, bed_file))

        try:

            read_csv(bed_file, "\t")

        except ValueError as e:
            bed_file_value_error_message = "the {} {} does not contain any data"
            raise ValueError(bed_file_value_error_message.format(file_type, bed_file)) from e
