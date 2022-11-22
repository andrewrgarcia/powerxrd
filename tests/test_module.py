import powerxrd as xrd
import numpy as np
import matplotlib.pyplot as plt

def test_isofncs():
    '''test isolated functions'''

    print(xrd.braggs(np.array([6.7,34.13,12.87]),lmda=1.54))
    print(xrd.braggs_s(2.3,lmda=1.54))
    print(xrd.scherrer(K=.9,lmda=2,beta=1,theta=24))

def test_backsub():
    
    data = xrd.Data('sample1.xy').importfile()
    chart = xrd.Chart(*data)

    chart.emission_lines(xrange_Ka=[10,20], show=True)
    plt.plot(*data,label='no backsub')
    plt.plot(*chart.backsub(),label='backsub')
    plt.xlabel('2 $\\theta$')
    plt.legend()
    # plt.suptitle('*all plots below are randomly-generated peaks (not real XRD data)')
    plt.show()

def test_sch():
    
    data = xrd.Data('sample1.xy').importfile()
    chart = xrd.Chart(*data)

    chart.backsub(tol=1.0,show=True)
    chart.SchPeak(xrange=[18,22],verbose=True, show=True)
    plt.xlabel('2 $\\theta$')
    plt.title('backsub and Scherrer width calculation')
    plt.show()


def test_allpeaks():
    
    data = xrd.Data('sample1.xy').importfile()
    chart = xrd.Chart(*data)

    chart.backsub(tol=1.0,show=True)
    chart.allpeaks(tols=(0.2,0.8),verbose=False, show=True)
    plt.xlabel('2 $\\theta$')
    plt.suptitle('backsub & Automated Scherrer width calculation of all peaks*')
    plt.show()


def test_mav():
    
    data = xrd.Data('sample1.xy').importfile()
    chart = xrd.Chart(*data)

    chart.backsub()
    n = 20
    plt.plot(*chart.mav(n))
    plt.xlabel('2 $\\theta$')
    plt.title('backsub and {}-point moving average'.format(n))
    plt.show()

test_isofncs()
test_backsub()
test_sch()
test_allpeaks()
test_mav()

