import numpy as np

def braggs(twotheta, lmda=1.54, is_scalar=False):
    '''
    Calculate interplanar spacing "d_hkl" from Bragg's law.
    - twotheta: Angle in degrees, can be a scalar or an array.
    - lmda: Wavelength in Angstroms, default is 1.54.
    - is_scalar: Flag to indicate if twotheta is a scalar (True) or an array (False).
    '''
    twothet_rad = twotheta * np.pi / 180

    if is_scalar:
        if twotheta < 5:
            return 'inf'
        else:
            dhkl = lmda / (2 * np.sin(twothet_rad / 2))
            return np.round(dhkl, 2)
    else:
        if np.any(twotheta < 5):
            L = len(twotheta)
            dhkl = np.zeros(L)
            dhkl[0] = np.inf

            for k in range(1, L):
                dhkl[k] = lmda / (2 * np.sin(twothet_rad[k] / 2)) if twotheta[k] >= 5 else 'inf'
        else:
            dhkl = lmda / (2 * np.sin(twothet_rad / 2))

        return np.round(dhkl, 2)

def scherrer(K,lmda,beta,theta):
    '''Scherrer equation'''
    # print('Scherrer Width == K*lmda / (FWHM*cos(theta))')
    return K*lmda / (beta*np.cos(theta))    #tau


def funcgauss(x,y0,a,mean,sigma):
    '''Gaussian equation'''
    return y0+(a/(sigma*np.sqrt(2*np.pi)))*np.exp(-(x-mean)**2/(2*sigma*sigma))

