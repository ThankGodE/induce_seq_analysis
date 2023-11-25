#!/bin/bash

#********************************************************************
#
# data_analysis_plotting_induce_seq.sh
# ${PROJECT_ROOT_REPOSITORY}/induce_seq_analysis_bash/data_analysis_plotting_induce_seq.sh
#
# PURPOSE
# ^^^^^^
#
# Script to process induce_seq files
#
#
#
# $Source: ${PROJECT_ROOT_REPOSITORY}/induce_seq_analysis_bash/data_analysis_plotting_induce_seq.sh
#*********************************************************************
# this is a strict mode for shell. it ensures that all commands exits with 0 and that all variables are set
set -e
set -u
#set -x for debugging


########################################################################################################################
# Help                                                                                                                 #
########################################################################################################################
Help() {

# Display Help
echo -e "Script to matrix file
Syntax: $0 [-o|-i|-d|-f|-h]
options
    -o    absolute directory path to processed output files
    -i    absolute directory to matrix file produced by process_induce_seq_matrix.py
    -d    absolute path to the Python script to process bam files: data_analysis_plotting_induce_seq.py .
          Default: ${ABSOLUTE_PATH_TO_ANALYSIS_PLOTTING_INDUCE_SEQ_PYTHON_SCRIPT};
    -f    force remove existing output files previously created. e.g. true or false. Default=false
    -h    Display Help";

}


########################################################################################################################
########################################################################################################################
# Main program                                                                                                         #
########################################################################################################################
########################################################################################################################
# Process the input options. Add the options as needed                                                                 #
########################################################################################################################

# Get the options
_get_bash_script_directory() {

  ABS_DIR_PATH_CURRENT_RUNNING_SCRIPT="$(dirname "$(realpath "$0")")";
  PARENT_DIR_ALL_SCRIPTS="$(dirname "$ABS_DIR_PATH_CURRENT_RUNNING_SCRIPT")";

  echo "$PARENT_DIR_ALL_SCRIPTS";

}
PROJECT_ROOT_DIRECTORY="$(_get_bash_script_directory)";

PATH_TO_MATRIX="";
PATH_TO_OUTPUT_DIRECTORY="";
REMOVE_PATH="false";
ABSOLUTE_PATH_TO_ANALYSIS_PLOTTING_INDUCE_SEQ_PYTHON_SCRIPT="$PROJECT_ROOT_DIRECTORY""/induce_seq_analysis_python/src/main/data_analysis_plotting_induce_seq.py";


while getopts i:o:d:f:h flag # the colon after any alphabet shows that an input argument is required.
do
    case "${flag}" in

    i) PATH_TO_MATRIX=${OPTARG};;
    o) PATH_TO_OUTPUT_DIRECTORY=${OPTARG};;
    d) ABSOLUTE_PATH_TO_ANALYSIS_PLOTTING_INDUCE_SEQ_PYTHON_SCRIPT=${OPTARG};;
    f) REMOVE_PATH="true";;
    h) Help
        exit;; # display Help
    \?) echo "Error: Invalid option  -${OPTARG}";
    exit;; # incorrect option

    esac
done



_check_mandatory_cli_arguments() {

  echo -e "checking mandatory commandline arguments...\n"

  if [ ! -d "${PATH_TO_OUTPUT_DIRECTORY}" ] || [ ! -d "${PATH_TO_MATRIX}" ] || \
        [ ! -f "${ABSOLUTE_PATH_TO_ANALYSIS_PLOTTING_INDUCE_SEQ_PYTHON_SCRIPT}" ] ; then
         echo -e "\nERROR: Options supplied to -o and -i must be directories that exists,
                  while -d must be a file that exists \n" >&2;
         Help
         exit 1
  fi

}

_remove_existing_matrix_files() {

  echo -e "removing existing files...\n";

  FORMER_PNG_FILE="$(find "$PATH_TO_OUTPUT_DIRECTORY" -type f -name "*.png" | wc -l)";

  if [ $REMOVE_PATH == "true" ] && [ -f "${FORMER_PNG_FILE}" ]; then

    rm "$FORMER_PNG_FILE";

  fi
}


_install_dependencies() {


  REQUIREMENTS_FILE="$PROJECT_ROOT_DIRECTORY/induce_seq_analysis_python/requirements.txt"

  echo $REQUIREMENTS_FILE

   python3 -m venv venv && \
   . venv/bin/activate && \
   pip install --upgrade pip && \
   pip install -r "$REQUIREMENTS_FILE"

}


_analyse_induce_seq() {

  echo -e "processing matrix file...\n";

  echo "venv/bin/python3 $ABSOLUTE_PATH_TO_ANALYSIS_PLOTTING_INDUCE_SEQ_PYTHON_SCRIPT -o $PATH_TO_OUTPUT_DIRECTORY -i $PATH_TO_MATRIX"

  venv/bin/python3 "${ABSOLUTE_PATH_TO_ANALYSIS_PLOTTING_INDUCE_SEQ_PYTHON_SCRIPT}" -o "${PATH_TO_OUTPUT_DIRECTORY}" -i "${PATH_TO_MATRIX}"

  deactivate

}
_main() {

echo -e "
path to output directory: $PATH_TO_OUTPUT_DIRECTORY
absolute directory to matrix file produced by process_induce_seq_matrix.py: $PATH_TO_MATRIX
absolute directory path to the Python script: $ABSOLUTE_PATH_TO_ANALYSIS_PLOTTING_INDUCE_SEQ_PYTHON_SCRIPT
force remove existing output files previously created: $REMOVE_PATH

"

_remove_existing_matrix_files;
_install_dependencies;
_analyse_induce_seq;

}

_main;
