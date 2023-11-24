"""
A collection of classes or functions that performs breaks processing operations
"""
import logging
import os.path
import sys

import pandas as pd

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

    def process_breaks(self) -> None:
        """ process breaks bed file """

        filtered_reads: object() = BreaksOperator.__filter_reads_from_breaks_file(self)
        path_to_filtered_file: str = os.path.join(self.output_directory, "filtered_reads.bed")

        file_writer: FileWriter = FileWriter(path_to_filtered_file, "w")
        file_writer.write_filtered_reads(filtered_reads)

        intersect: pd.DataFrame = BreaksOperator.__intersect_breaks_with_asisi(self, path_to_filtered_file)

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
            asisi_breaks_merged_df["start_asisi"].astype(int) <= asisi_breaks_merged_df["start_breaks"].astype(int)]

        asisi_breaks_merged_df = asisi_breaks_merged_df[asisi_breaks_merged_df["end_asisi"].astype(int) >=
                                                        asisi_breaks_merged_df["end_breaks"].astype(int)]

        sum_asisi_breaks = len(list(asisi_breaks_merged_df["start_breaks"]))
        total_non_filtered_breaks = len(read_csv(self.breaks_file, Delimiters.TAB_SEPERATOR))
        normalised_number_asisi_breaks = sum_asisi_breaks / (total_non_filtered_breaks / 1000)

        print(sum_asisi_breaks)
        print(total_non_filtered_breaks)
        print(normalised_number_asisi_breaks)

        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_columns', None)
        pd.get_option("display.max_rows", None)
        pd.set_option('display.width', None)

        print(asisi_breaks_merged_df.head(10), "OOOO")

        sys.exit()

    def __filter_reads_from_breaks_file(self) -> object():
        """ filter reads from a breaks bed file """

        for row in read_csv(self.breaks_file, Delimiters.TAB_SEPERATOR):
            if BreaksOperator.__filter_read_from_breaks_row(row, self.score_threshold):
                yield row

    @classmethod
    def __filter_read_from_breaks_row(cls, line: str, threshold: int) -> bool:
        """ filter reads from a breaks bed line """

        return int(line[Positions.FIFTH]) >= threshold
