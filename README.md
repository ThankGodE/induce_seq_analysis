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

## 2. Edit only one line in the NextFlow ```analyse_induce_seq.config``` file by replacing the path variable string of ```env.PROJECT_CODE_BASE_SRC_DIR``` with the absolute path ```(i.e. the output of pwd)``` of pwd from above

```
vim induce_seq_analysis_nextflow/analyse_induce_seq.config
```

If the absolute path for the input and output directories changes, please edit the process_bam_file.config file accordingly to reflect these new paths.

## 3. then run NextFlow - entry point of the pipeline:

### Example

```
nextflow run induce_seq_analysis_nextflow/analyse_induce_seq.nf -c induce_seq_analysis_nextflow/analyse_induce_seq.config -with-singularity
```

### Check outputs

The plot, filtered breaks, and filtered asisi breaks will be located in ```resources/example_data/output/```:

To get the plot, please do:

```
ls -l resources/example_data/output/*png
```

To get the filtered breaks, please do:

```
ls -l resources/example_data/output/*filtered_reads.bed
```

To get the normalised asisi breaks

```
ls -l resources/example_data/output/*normalised_asisi_breaks.tsv
```

# Answers to the questions: 

The answers to the questions are based on the interpretation of the PNG file here: `ls -l resources/example_data/output/*png`

1. Which of the samples are likely to be controls or treated?

    #### TGE response: Controls are Sample IDs 4, 2, 1, 5, 6, 8, and 7


2. Are there any you are uncertain of?

   #### TGE response: Sample ID 3 is uncertain


3. Can you explain the samples in the uncertain group?

    #### TGE response: Majority of the samples in the uncertain group have MAPQ < 30. Only one have MAPQ > 30 and this seems to disappear with normalisation


4. Of all the possible AsiSI sites described in the chr21_AsiSI_sites.t2t.bed file what is the maximum percentage observed in a single sample?

   #### TGE response: Maximum % observed in a single sample is 0.48 % in Sample 11

 
