#!/usr/bin/env nextflow

params.output_directory = "$params.path_to_output_directory"
params.absolute_path_project_root_dir = "$params.absolute_path_to_project_root_dir_source"
params.path_to_breaks_bed_files = "$params.path_to_breaks_bed_files"
params.path_to_asisi_bed_file = "$params.path_to_asisi_bed_file"

// create channels for breaks bed files
breaks_bed_files_ch = Channel.fromFilePairs("${params.path_to_breaks_bed_files}/**.${params.breaks_bed_file_extension}", checkIfExists: true, size: -12, followLinks: true)

process PROCESS_INDUCE_SEQ() {

    publishDir params.output_directory, mode:'copy'
    input:
    tuple val(sample_id), path(breaks_bed_file)

    output:
    val "process_asisi_breaks_completed"

    shell:
    """
    $params.absolute_path_project_root_dir/induce_seq_analysis_bash/process_induce_seq.sh \
    -o $params.output_directory -i $params.path_to_breaks_bed_files/$breaks_bed_file -a $params.path_to_asisi_bed_file \
    -s $sample_id
    """

}

process COMBINE_ASISI_BREAKS() {

    publishDir params.output_directory, mode:'copy'
    input:
    val process_induce_completed

    output:
    val "$params.output_directory/merged_normalised_asisi_breaks_matrix.csv"

    shell:
    """
    find $params.output_directory/ -type f -name '*normalised_asisi_breaks.bed' -exec cat {} + \
      | sort -u -V | grep number_asisi_breaks > $params.output_directory/merged_normalised_asisi_breaks_matrix.csv

   find $params.output_directory/ -type f -name '*normalised_asisi_breaks.bed' -exec cat {} + \
   | grep -v number_asisi_breaks >> $params.output_directory/merged_normalised_asisi_breaks_matrix.tsv
    """
}

process ANALYSE_ASISI_BREAKS() {

    publishDir params.output_directory, mode:'copy'
    input:
    val merged_normalised_asisi_breaks_matrix

    output:
    val"analyse_asisi_completed"

    shell:
    """
    $params.absolute_path_project_root_dir/induce_seq_analysis_bash/data_analysis_plotting_induce_seq.sh \
    -o $params.output_directory -i $merged_normalised_asisi_breaks_matrix
    """

}



workflow() {

    process_asisi_breaks_ch = PROCESS_INDUCE_SEQ(breaks_bed_files_ch)
    combine_asisi_breaks_ch = COMBINE_ASISI_BREAKS(process_asisi_breaks_ch.collect())
    analyse_asisi_breaks_ch = ANALYSE_ASISI_BREAKS(combine_asisi_breaks_ch)

}

