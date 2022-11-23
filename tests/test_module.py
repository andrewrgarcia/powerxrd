import powerxrd as xrd
import numpy as np
import matplotlib.pyplot as plt

def test_isofncs():
    '''test isolated functions'''

    print(xrd.braggs(np.array([6.7,34.13,12.87]),lmda=1.54))
    print(xrd.braggs_s(2.3,lmda=1.54))
    print(xrd.scherrer(K=.9,lmda=2,beta=1,theta=24))


def test_backsub_multiplt():
    

    fig, axs = plt.subplots(6, 1, sharex=True)
    fig.subplots_adjust(hspace=0)

    # xrd.Data import tab-separated files (.xy) file witn importfile() 
    for i in range(2):
        data = xrd.Data('synthetic-data/sample{}.xy'.format(i)).importfile()
        chart = xrd.Chart(*data)
        axs[i].plot(*chart.backsub(),color='k',label='sample{}.xy'.format(i))
        axs[i].legend()


    # xrd.Data can now also import csv file with .importfile('csv') option 
    for j in range(2):
        for i in range(1,5):
            data = xrd.Data('synthetic-data/sample{}.csv'.format(i+j-1)).importfile('csv')
            chart = xrd.Chart(*data)
            axs[i+1].plot(*chart.backsub(),color='C'+str(i+j-1),label='sample{}.csv'.format(i+j-1))
            axs[i+1].legend()


    plt.xlabel('2 $\\theta$')
    # plt.suptitle('*all plots below are from synthetic data (i.e. not real XRD)')
    axs[0].set_title('imported from different formats (.xy and .csv)')
    plt.show()


def test_backsub_emission():
    
    data = xrd.Data('synthetic-data/sample1.xy').importfile()
    chart = xrd.Chart(*data)

    chart.emission_lines(xrange_Ka=[10,20], show=True)
    plt.plot(*data,label='no backsub')
    plt.plot(*chart.backsub(),label='backsub')
    plt.xlabel('2 $\\theta$')
    plt.legend()
    # plt.suptitle('*all plots below are from synthetic data (i.e. not real XRD)')
    plt.show()

def test_sch():
    
    data = xrd.Data('synthetic-data/sample1.xy').importfile()
    chart = xrd.Chart(*data)

    chart.backsub(tol=1.0,show=True)
    chart.SchPeak(xrange=[18,22],verbose=True, show=True)
    plt.xlabel('2 $\\theta$')
    plt.title('backsub and Scherrer width calculation')
    plt.show()


def test_allpeaks():
    
    data = xrd.Data('synthetic-data/sample1.xy').importfile()
    chart = xrd.Chart(*data)

    chart.backsub(tol=1.0,show=True)
    chart.allpeaks(tols=(0.2,0.8),verbose=False, show=True)
    plt.xlabel('2 $\\theta$')
    plt.suptitle('backsub & Automated Scherrer width calculation of all peaks*')
    plt.show()


def test_mav():
    
    data = xrd.Data('synthetic-data/sample1.xy').importfile()
    chart = xrd.Chart(*data)

    chart.backsub()
    n = 20
    plt.plot(*chart.mav(n))
    plt.xlabel('2 $\\theta$')
    plt.title('backsub and {}-point moving average'.format(n))
    plt.show()

test_isofncs()
test_backsub_multiplt()
test_backsub_emission()
test_sch()
test_allpeaks()
test_mav()

