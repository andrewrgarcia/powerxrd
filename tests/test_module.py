from lib import module as xrd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def test_backsub():
    
    df = pd.read_csv('sample1.xy', sep='\t', header=None)   #'https://www.statology.org/pandas-read-text-file/'
    x,y = np.array(df).T
    x,y = xrd.backsub(x,y)
    
    plt.plot(x,y,label='sample1.xy')
    plt.xlabel('2 $\\theta$')
    plt.legend()
    

test_backsub()