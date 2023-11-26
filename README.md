# Induce Seq Analysis
Pipeline to process and analyse INDUCE-seq data

This script - analyse_induce_seq.nf:
1. Filter out reads that have a mapping quality of < 30
2. Intersect each sample break bed file with the AsiSI site bed file
3. Sum and normalise the counts
4. Collect normalised number of AsiSI breaks
5. Plot the results: determine which samples are most likely to represent the control and treated subsets. 
6. Takes the pipeline output of process_induce_seq.py and plots a line graph of asisi breaks

Required:
- NextFlow


# Usage

# RUN PIPELINE

The below step outlines how to run this NextFlow pipeline: analyse_induce_seq.nf

## 1. Set up the environment

```
git clone https://github.com/ThankGodE/induce_seq_analysis.git
```
```
cd induce_seq_analysis
```
```
pwd
```

## 2. edit only one line in the NextFlow ```analyse_induce_seq.config``` file by replacing the path variable string of ```env.PROJECT_CODE_BASE_SRC_DIR``` with the absolute path ```(i.e. the output of pwd)``` of pwd from above

```
vim induce_seq_analysis_nextflow/analyse_induce_seq.config
```

If the absolute path for the input and output directories changes, please edit the process_bam_file.config file accordingly to reflect these new paths.

## 3. then run NextFlow - entry point of the pipeline:

### Example

```
nextflow run induce_seq_analysis_nextflow/analyse_induce_seq.nf -c induce_seq_analysis_nextflow/analyse_induce_seq.config -with-singularity
```