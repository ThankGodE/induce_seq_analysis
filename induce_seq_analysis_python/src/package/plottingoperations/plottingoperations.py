"""
A collection of classes or functions that performs plotting operations
"""
import os

import pandas as pd
import matplotlib.pyplot as plt

from package.enumsoperations.character_enums import Words
from package.enumsoperations.delimiter_enums import Delimiters


class PlottingOperator:
    """ A class that performs plotting operations   """

    matrix_file = None
    output_directory = None

    def __init__(self, matrix_file: str, output_directory: str) -> None:
        """ Constructor

       Parameters
      ----------
      matrix_file:str
          The file that contains the matrix to be plotted
      output_directory:str
          The directory where the output will be stored
          """

        self.matrix_file = matrix_file
        self.output_directory = output_directory

    def plot_matrix(self) -> None:
        """ Plots the matrix contained in the file specified in the constructor """

        matrix_df = pd.read_csv(self.matrix_file, sep=Delimiters.TAB_SEPERATOR)

        plt.plot(
            matrix_df[Words.BreaksAsisiColumNames.SAMBPLE_ID].str.replace("Sample", "").str.replace(".breakends", ""),
            matrix_df[Words.BreaksAsisiColumNames.NORMALISED_NUMBER_ASISI_BREAKS])

        plt.xlabel("Sample ID")
        plt.ylabel("Normalised number of ASISI breaks")
        plt.title("ASISI breaks")
        plt.savefig(os.path.join(self.output_directory, "normalised_number_of_asis_breaks.png"))
        plt.clf()
