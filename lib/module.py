import numpy as np

def backsub(x,y,tol=1):
    '''Background subtraction operation
    inputs:
        x - x-data (e.g. 2Theta values)
        y - y-data (e.g. Intensity)
        tol - tolerance (see below)
    outputs: 
        x
        y
    
    This function is a running conditional statement 
    which evaluates whether a small increase 
    in the x-direction will increase the magnitude of the 
    y variable beyond a certain tolerance
    
    this tolerance ('tol') value may be adjusted as an input'''
    
    L=len(y)
    lmda = int(0.50*L/(x[0]-x[L-1]))         #   'approx. # points for half width of peaks'

    backsub_y=np.zeros(L)
    for i in range(L):
        if y[(i+lmda)%L] > tol*y[i]:          #tolerance 'tol'
            backsub_y[(i+lmda)%L] = y[(i+lmda)%L] - y[i]
        else:
            if y[(i+lmda)%L] < y[i]:
                backsub_y[(i+lmda)%L] = 0

    return x,backsub_y
    
    
