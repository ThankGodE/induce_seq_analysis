"""
This script:
    1. Filter out reads that have a mapping quality of < 30
    2. Intersect each sample break bed file with the AsiSI site bed file
    3. Sum and normalise the counts
    4. Collect normalised number of AsiSI breaks
    5. Plot the results: determine which samples are most likely to represent the control and treated subsets.

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


from package.profiling.profiling import begin_profiling, end_profiling, ProfileLogger
from package.breaksoperation.breaksoperations import BreaksOperator
from package.commandlineoperations.commandline_input_argument_getter import CliInputArgumentGetter


profiling_starting = begin_profiling("")

###################################################
# main function                               #####
###################################################


def main() -> None:
    """main function to run commandline arguments and call other functions to run."""

    args_cli_values = CliInputArgumentGetter.get_cli_input_arguments()

    CliInputArgumentGetter.check_input_arguments(args_cli_values)

    path2output_dir = args_cli_values.path2out
    path2breaks_files = args_cli_values.path2breaks
    path2asisi = args_cli_values.path2asisi
    # bed_file_extension = args_cli_values.bed_extension
    mapping_score = args_cli_values.score_threshold

    try:

        breaks_operator: BreaksOperator = BreaksOperator(path2breaks_files, path2asisi, path2output_dir, mapping_score)
        breaks_operator.process_breaks()

        # all_breaks_files: list = globally_get_all_files(path2breaks_files, bed_file_extension)
        # bed_file: str = get_first_element(globally_get_all_files(path2bed, bed_file_extension))

        # bam_operator: BamOperator = BamOperator(all_bam_files, bed_file, path2output_dir)
        #
        # bam_operator.process_bam_files()

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

