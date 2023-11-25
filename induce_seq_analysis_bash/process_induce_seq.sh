#!/bin/bash

#********************************************************************
#
# process_induce_seq.sh
# ${PROJECT_ROOT_REPOSITORY}/induce_seq_analysis_bash/process_induce_seq.sh
#
# PURPOSE
# ^^^^^^
#
# Script to process induce_seq files
#
#
#
# $Source: ${PROJECT_ROOT_REPOSITORY}/induce_seq_analysis_bash/process_induce_seq.sh
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
echo -e "Script to process bed files
Syntax: $0 [-o|-i|-p|-s|-c|-h]
options
    -o    absolute directory path to processed output files
    -i    absolute directory breaks bed files
    -a    absolute file path to AsiSI sites bed file
    -s    sample ids
    -d    absolute path to the Python script to process bam files: process_induce_seq.py .
          Default: ${ABSOLUTE_PATH_TO_PROCESS_INDUCE_SEQ_PYTHON_SCRIPT};
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

PATH_TO_BREAKS_FILES="";
PATH_TO_OUTPUT_DIRECTORY="";
PATH_TO_ASISI_BED_FILE="";
SAMPLE_ID="";
REMOVE_PATH="false";
ABSOLUTE_PATH_TO_PROCESS_INDUCE_SEQ_PYTHON_SCRIPT="$PROJECT_ROOT_DIRECTORY""/induce_seq_analysis_python/src/main/process_induce_seq.py";


while getopts i:o:d:a:s:f:h flag # the colon after any alphabet shows that an input argument is required.
do
    case "${flag}" in

    i) PATH_TO_BREAKS_FILES=${OPTARG};;
    o) PATH_TO_OUTPUT_DIRECTORY=${OPTARG};;
    d) ABSOLUTE_PATH_TO_PROCESS_INDUCE_SEQ_PYTHON_SCRIPT=${OPTARG};;
    a) PATH_TO_ASISI_BED_FILE=${OPTARG};;
    s) SAMPLE_ID=${OPTARG};;
    f) REMOVE_PATH="true";;
    h) Help
        exit;; # display Help
    \?) echo "Error: Invalid option  -${OPTARG}";
    exit;; # incorrect option

    esac
done


_check_mandatory_cli_arguments() {

  echo -e "checking mandatory commandline arguments...\n"

  if [ ! -d "${PATH_TO_OUTPUT_DIRECTORY}" ] || [ ! -d "${PATH_TO_BREAKS_FILES}" ] || [ ! -f "${PATH_TO_ASISI_BED_FILE}" ] ||
        [ ! -f "${ABSOLUTE_PATH_TO_PROCESS_INDUCE_SEQ_PYTHON_SCRIPT}" ] ; then
         echo -e "\nERROR: Options supplied to -o and -i must be directories that exists,
                  while -a must be a file that exists \n" >&2;
         Help
         exit 1
  fi

}

_remove_existing_matrix_files() {

  echo -e "removing existing files...\n";

  FORMER_MATRIX_FILE="$(find "$PATH_TO_OUTPUT_DIRECTORY" -type f -name "*.csv" | wc -l)";

  if [ $REMOVE_PATH == "true" ] && [ -f "${FORMER_MATRIX_FILE}" ]; then

    rm "$FORMER_MATRIX_FILE";

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

_process_induce_seq() {


  echo -e "processing bed files...\n";

  echo "venv/bin/python3 $ABSOLUTE_PATH_TO_PROCESS_INDUCE_SEQ_PYTHON_SCRIPT -o $PATH_TO_OUTPUT_DIRECTORY -i $PATH_TO_BREAKS_FILES \
    -a $PATH_TO_ASISI_BED_FILE -s $SAMPLE_ID"

  venv/bin/python3 "${ABSOLUTE_PATH_TO_PROCESS_INDUCE_SEQ_PYTHON_SCRIPT}" -o "${PATH_TO_OUTPUT_DIRECTORY}" -i "${PATH_TO_BREAKS_FILES}" \
  -a "${PATH_TO_ASISI_BED_FILE}" -s "${SAMPLE_ID}"

  deactivate

}

_main() {

echo -e "
path to output directory: $PATH_TO_OUTPUT_DIRECTORY
absolute directory breaks bed files: $PATH_TO_BREAKS_FILES
absolute file path to AsiSI sites bed file: $PATH_TO_ASISI_BED_FILE
sample id: $SAMPLE_ID
absolute directory path to the Python script: $ABSOLUTE_PATH_TO_PROCESS_INDUCE_SEQ_PYTHON_SCRIPT
force remove existing output files previously created: $REMOVE_PATH

"

_remove_existing_matrix_files;
_install_dependencies;
_process_induce_seq;

}

_main;