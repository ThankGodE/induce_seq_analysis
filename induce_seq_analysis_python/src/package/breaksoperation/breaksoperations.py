"""
A collection of classes or functions that performs breaks processing operations
"""
import logging
import os.path
import sys

import pandas as pd

from package.datastructureoperations.listoperations.listhandlers import get_first_element
from package.enumsoperations.character_enums import Words
from package.enumsoperations.delimiter_enums import Delimiters
from package.enumsoperations.numerical_enums import Positions
from package.fileoperations.filehandlers import read_csv
from package.fileoperations.filewriters import FileWriter


class BreaksOperator:
    """Performs breaks processing operations"""

    breaks_bed_file = None
    asisi_file = None
    output_directory = None
    score_threshold = None

    def __init__(self, breaks_file: str, asisi_file: str, output_directory: str, score_threshold: int) -> None:
        """
        Constructor

        Parameters
        ----------
        breaks_file :str
           Path to breaks file
        asisi_file:str
           Path to asisi file
        output_directory:str
           Path to output directory
        """

        self.breaks_file = breaks_file
        self.asisi_file = asisi_file
        self.output_directory = output_directory
        self.score_threshold = score_threshold

    def process_breaks(self, sample_identifier) -> None:
        """ process breaks bed file """

        filter_file_basename = sample_identifier + "_filtered_reads.bed"
        normalised_asisi_breaks_basename = sample_identifier + "_normalised_asisi_breaks.bed"

        path_to_filtered_file: str = os.path.join(self.output_directory, filter_file_basename)
        path_to_normalised_number_asisi_breaks_file: str = os.path.join(self.output_directory,
                                                                        normalised_asisi_breaks_basename)

        filtered_reads: object() = BreaksOperator.__filter_reads_from_breaks_file(self)
        file_writer: FileWriter = FileWriter(path_to_filtered_file, "w")
        file_writer.write_filtered_reads(filtered_reads)

        breaks_file_asisi_sites_intersect_df: pd.DataFrame = (
            BreaksOperator.__intersect_breaks_with_asisi(self, path_to_filtered_file))
        normalised_asisi_sum_df: pd.DataFrame = BreaksOperator.__sum_normalise_counts_asisi_breaks(
            self, breaks_file_asisi_sites_intersect_df)
        file_writer_normalised_sum: FileWriter = FileWriter(path_to_normalised_number_asisi_breaks_file, "w")
        file_writer_normalised_sum.write_df(normalised_asisi_sum_df, Delimiters.TAB_SEPERATOR, True)

    def __intersect_breaks_with_asisi(self, breaks_bed_file: str) -> pd.DataFrame:
        """ intersect breaks bed file with asisi bed file """

        breaks_file_content_df: pd.DataFrame = pd.read_csv(breaks_bed_file, sep=Delimiters.TAB_SEPERATOR, header=None,
                                                           names=[Words.BreaksAsisiColumNames.CHROMOSOME,
                                                                  Words.BreaksAsisiColumNames.START,
                                                                  Words.BreaksAsisiColumNames.END,
                                                                  Words.BreaksAsisiColumNames.BED_LINE_NAME,
                                                                  Words.BreaksAsisiColumNames.SCORE,
                                                                  Words.BreaksAsisiColumNames.STRAND])

        asisi_file_content_df: pd.DataFrame = pd.read_csv(self.asisi_file, sep=Delimiters.TAB_SEPERATOR, header=None,
                                                          names=[Words.BreaksAsisiColumNames.CHROMOSOME,
                                                                 Words.BreaksAsisiColumNames.START,
                                                                 Words.BreaksAsisiColumNames.END])

        asisi_breaks_merged_df = pd.merge(asisi_file_content_df, breaks_file_content_df,
                                          on=Words.BreaksAsisiColumNames.CHROMOSOME, suffixes=(
                Words.BreaksAsisiColumNames.ASISI_SUFFIX, Words.BreaksAsisiColumNames.BREAKS_SUFFIX))

        asisi_breaks_merged_df = asisi_breaks_merged_df[
            asisi_breaks_merged_df[Words.BreaksAsisiColumNames.START_ASISI].astype(int) <= asisi_breaks_merged_df[
                Words.BreaksAsisiColumNames.START_BREAKS].astype(int)]

        asisi_breaks_merged_df = asisi_breaks_merged_df[
            asisi_breaks_merged_df[Words.BreaksAsisiColumNames.END_ASISI].astype(int) >= asisi_breaks_merged_df[
                Words.BreaksAsisiColumNames.END_BREAKS].astype(int)]

        return asisi_breaks_merged_df

    def __sum_normalise_counts_asisi_breaks(self, asisi_breaks_df: pd.DataFrame) -> pd.DataFrame:
        """ Sum and normalise the number of asisi breaks to the total number of breaks. """

        sum_asisi_breaks = len(list(asisi_breaks_df["start_breaks"]))
        total_non_filtered_breaks = len(read_csv(self.breaks_file, Delimiters.TAB_SEPERATOR))
        normalised_number_asisi_breaks = sum_asisi_breaks / (total_non_filtered_breaks / 1000)

        return pd.DataFrame(
            {Words.BreaksAsisiColumNames.NUMBER_NON_FILTERED_BREAKS: [total_non_filtered_breaks],
             Words.BreaksAsisiColumNames.NUMBER_ASISI_BREAKS: [sum_asisi_breaks],
             Words.BreaksAsisiColumNames.NORMALISED_NUMBER_ASISI_BREAKS: [normalised_number_asisi_breaks]})

    def __filter_reads_from_breaks_file(self) -> object():
        """ filter reads from a breaks bed file """

        for row in read_csv(self.breaks_file, Delimiters.TAB_SEPERATOR):
            if BreaksOperator.__filter_read_from_breaks_row(row, self.score_threshold):
                yield row

    @classmethod
    def __filter_read_from_breaks_row(cls, line: str, threshold: int) -> bool:
        """ filter reads from a breaks bed line """

        return int(line[Positions.FIFTH]) >= threshold
