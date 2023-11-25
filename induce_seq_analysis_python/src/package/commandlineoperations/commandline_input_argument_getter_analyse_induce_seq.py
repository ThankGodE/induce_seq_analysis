"""
A collection of classes or functions that grabs commandline arguments
"""

__name__ = "__main__"

import argparse
import os


class CliInputArgumentGetter:
    """Wrapper for argparse that returns an object of the class for ease of use"""

    @classmethod
    def get_cli_input_arguments(cls, args=None) -> argparse.Namespace:
        """gets input arguments from the commandline interface """

        parser = argparse.ArgumentParser(prog="data_analysis_plotting_induce_seq.py",
                                         usage="""data_analysis_plotting_induce_seq.py -h""",
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=("""
                    This script:
                        Takes the pipeline output of process_induce_seq.py and plots a line graph for asisi breaks

                    Required:
                        - Python >= 3.10
                        - python-dotenv>=1.0.0
                        - for additional dependencies, see requirements.txt

                """), )
        parser.add_argument("-o", "--path2out", help="absolute directory path to processed output files ",
                            required=True, )
        parser.add_argument("-i", "--path2matrix", help="""absolute path to input matrix file containing sample name, 
                            number of breaks, number of asisi breaks, and normalised asisi breaks. For example:
                            
                            sample_id	number_non_filtered_breaks	number_asisi_breaks	normalised_number_asisi_breaks
                            Sample9.breakends	1826	5	2.7382256297918945
                            Sample16.breakends	5347	18	3.36637366747709""",
                            required=True, type=str)

        return parser.parse_args(args)

    @classmethod
    def check_input_arguments(cls, cli_input_arguments: argparse.Namespace) -> None:
        """ check or verify input arguments """

        if not os.path.exists(cli_input_arguments.path2matrix) and not os.path.isfile(cli_input_arguments.path2matrix):
            matrix_path_error_message = "asisi matrix file {} does not exist!"
            raise FileNotFoundError(matrix_path_error_message.format(cli_input_arguments.path2matrix))

        if not os.path.exists(cli_input_arguments.path2out) and not os.path.isfile(cli_input_arguments.path2output):
            output_path_error_message = "output directory {} does not exist!"
            raise FileNotFoundError(output_path_error_message.format(cli_input_arguments.path2output))
