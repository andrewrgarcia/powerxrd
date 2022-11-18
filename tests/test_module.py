import powerxrd as xrd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def test_isofncs():
    '''test isolated functions'''

    print(xrd.braggs(np.array([6.7,34.13,12.87]),lmda=1.54))
    print(xrd.braggs_s(2.3,lmda=1.54))
    print(xrd.scherrer(K=.9,lmda=2,beta=1,theta=24))

def test_backsub():
    
    df = pd.read_csv('sample1.xy', sep='\t', header=None)   #'https://www.statology.org/pandas-read-text-file/'
    x,y = np.array(df).T

    chart = xrd.Chart(x,y)

    chart.emission_lines(show=True)
    plt.plot(x,y,label='no backsub')
    plt.plot(*chart.backsub(),label='backsub')
    plt.xlabel('2 $\\theta$')
    plt.legend()
    # plt.suptitle('*all plots below are randomly-generated peaks (not real XRD data)')
    plt.show()

def test_sch():
    
    df = pd.read_csv('sample1.xy', sep='\t', header=None)   #'https://www.statology.org/pandas-read-text-file/'
    x,y = np.array(df).T

    chart = xrd.Chart(x,y)

    chart.backsub(tol=1.0,show=True)
    chart.SchPeak(show=True,xrange=[18,22])
    plt.xlabel('2 $\\theta$')
    plt.title('backsub and Scherrer width calculation')
    plt.show()



def test_mav():
    
    df = pd.read_csv('sample1.xy', sep='\t', header=None)   #'https://www.statology.org/pandas-read-text-file/'
    x,y = np.array(df).T

    chart = xrd.Chart(x,y)

    chart.backsub()
    n = 20
    plt.plot(*chart.mav(n))
    plt.xlabel('2 $\\theta$')
    plt.title('backsub and {}-point moving average'.format(n))
    plt.show()

test_isofncs()
test_backsub()
test_sch()
test_mav()

