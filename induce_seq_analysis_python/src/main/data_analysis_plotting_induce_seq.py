"""
This script:
    Takes the pipeline output of process_induce_seq.py and plots a line graph of asisi breaks

Required:
    - Python >= 3.10
    - python-dotenv>=1.0.0
    - for additional dependencies, see requirements.txt
"""

# Futures local application libraries, source package
from addscriptdir2path import add_package2env_var

# re-define system path to include modules, packages
# and libraries in environment variable
add_package2env_var()

from package.commandlineoperations.commandline_input_argument_getter_analyse_induce_seq import CliInputArgumentGetter
from package.plottingoperations.plottingoperations import PlottingOperator

from package.profiling.profiling import begin_profiling, end_profiling, ProfileLogger

profiling_starting = begin_profiling("")

###################################################
# main function                               #####
###################################################


def main() -> None:
    """main function to run commandline arguments and call other functions to run."""

    args_cli_values = CliInputArgumentGetter.get_cli_input_arguments()

    CliInputArgumentGetter.check_input_arguments(args_cli_values)

    path2output_dir = args_cli_values.path2out
    path2asisimatrix = args_cli_values.path2matrix

    try:

        plotting_operation: PlottingOperator = PlottingOperator(path2asisimatrix, path2output_dir)
        plotting_operation.plot_matrix()

    except (ValueError, TypeError, FileNotFoundError) as e:

        if isinstance(e, ValueError):
            raise ValueError(e) from e

        if isinstance(e, TypeError):
            raise TypeError(e) from e

        if isinstance(e, FileNotFoundError):
            raise FileNotFoundError(e) from e


###################################################################################
# run __main__ ####################################################################
###################################################################################
if __name__ == "__main__":
    main()

time_end = end_profiling()
ProfileLogger(profiling_starting, time_end).log_profiling()

