import numpy as np
import pandas

class Data:
    def __init__(self,file):
        '''
        Data structure.

        Parameters
        ----------
        file : str
            file name and/or path for XRD file in .xy format
        '''
        self.file = file
        self.refinement_flags = None  # New attribute to store flags for refinement

    def set_refinement_flags(self, indices, flag):
        if self.refinement_flags is None:
            self.refinement_flags = [True] * len(self.x)  # Initialize all flags to True
        for index in indices:
            self.refinement_flags[index] = flag

    def get_refinable_data(self):
        if self.refinement_flags is None:
            return self.x, self.y  # If no flags are set, all data is refinable
        else:
            return self.x[self.refinement_flags], self.y[self.refinement_flags]

    def importfile(self):

        if self.file.split(".")[1]=='xy':
            df = pandas.read_csv(self.file, sep=r'\s+', header=None)   #'https://www.statology.org/pandas-read-text-file/'

        if self.file.split(".")[1]=='csv':
            df = pandas.read_csv(self.file, header=None)   

        x,y = np.array(df).T
        return x,y 