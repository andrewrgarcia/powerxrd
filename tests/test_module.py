import powerxrd as xrd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def test_backsub():
    
    df = pd.read_csv('sample1.xy', sep='\t', header=None)   #'https://www.statology.org/pandas-read-text-file/'
    x,y = np.array(df).T

    chart = xrd.Chart(x,y)
    # x,y = chart.backsub()
    chart.emission_lines(show=True)
    plt.plot(x,y,label='no backsub')
    plt.plot(*chart.backsub(),label='backsub')
    plt.xlabel('2 $\\theta$')
    plt.legend()
    plt.show()


test_backsub()
