import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize


'''interplanar spacing "d_hkl" from Braggs law'''
def braggs(twotheta,lmda=1.54):
    'lambda in Angstroms'
    twothet_rad=twotheta*np.pi/180
    
#    dhkl = lmda /(2*np.sin(twothet_rad/2))
    
    if twotheta.any() < 5:
        L =len(twotheta)
        dhkl = np.zeros(L)
        dhkl[0] = 'inf'
        
        k =1
        while k < L:
            dhkl[k] = lmda /(2*np.sin(twothet_rad[k]/2))
            k+=1
    else:
        dhkl = lmda /(2*np.sin(twothet_rad/2))
    
    dhkl = np.round(dhkl,2)
    return dhkl

def braggs_s(twotheta,lmda=1.54):
    'lambda in Angstroms'
    twothet_rad=twotheta*np.pi/180
    
    
    if twotheta < 5:
        dhkl = 'inf'
    else:
        dhkl = lmda /(2*np.sin(twothet_rad/2))
        dhkl = np.round(dhkl,2)
    

    return dhkl


'''Scherrer equation'''
def scherrer(K,lmda,beta,theta):

    print('Scherrer Width == K*lmda / (FWHM*cos(theta))')
    return K*lmda / (beta*np.cos(theta))    #tau


'''Gaussian fit for FWHM'''
def funcgauss(x,y0,a,mean,sigma):
    
    return y0+(a/(sigma*np.sqrt(2*np.pi)))*np.exp(-(x-mean)**2/(2*sigma*sigma))

#def funcgauss(x,y0,a,mean,fwhm):

#    return y0 + (a/(fwhm*np.sqrt(np.pi/(4*np.log(2)) )))*np.exp(-(4*np.log(2))*(x-mean)**2/(fwhm*fwhm))



class Chart:

    def __init__(self,x,y):
        '''Model structure. Calls `3-D` array to process into 3-D model.

        Parameters
        ----------
        array : np.array(int)
            array of the third-order populated with discrete, non-zero integers which may represent a voxel block type
        hashblocks : dict[int]{str, float }
            a dictionary for which the keys are the integer values on the discrete arrays (above) an the values are the color (str) for the specific key and the alpha for the voxel object (float)
        '''
        self.x = x          # x values
        self.y = y          # y values

    '''Local maxima finder'''
    def local_max(self,xrange=[12,13]):
        x1,x2=xrange
        xsearch_index=[]
        for n in self.x:
            if n >= x1 and  n <= x2:
                xsearch_index.append(list(self.x).index(n))

        max_y = 0
        max_x = 0
        for i in xsearch_index:
            if self.y[i] > max_y:
                max_y = self.y[i]
                max_x = self.x[i]

        return max_x, max_y

    '''Emission lines arising from different types of radiation i.e. K_beta radiation
    wavelength of K_beta == 0.139 nm'''
    def emission_lines(self, show = True, twothet_range_Ka=[10,20], lmda_Ka = 0.154,lmda_Ki=0.139):

        twothet_Ka_deg, int_Ka = Chart(self.x, self.y).local_max(xrange=twothet_range_Ka)
        twothet_Ka=twothet_Ka_deg*np.pi/180

        twothet_Ki = 2*np.arcsin((lmda_Ki/lmda_Ka)*np.sin(twothet_Ka/2))
        twothet_Ki_deg = twothet_Ki*180/np.pi

        # return twothet_Ka_deg, int_Ka, twothet_Ki_deg

        if show:
            plt.vlines(twothet_Ka_deg,0,int_Ka, colors='k', linestyles='solid', \
                    label=r'K$\alpha$; $\theta$ = {} '.format(round(twothet_Ka_deg,2)))
            plt.vlines((twothet_Ka_deg+twothet_Ki_deg)/2,0,int_Ka, colors='k', linestyles='--', label='')
            plt.vlines(twothet_Ki_deg,0,int_Ka, colors='r', linestyles='solid',\
                    label=r'K$\beta$; $\theta$ = {} '.format(round(twothet_Ki_deg,2)))
        else:

            return twothet_Ki_deg


    def gaussfit(self):
        meanest = self.x[list(self.y).index(max(self.y))]
        sigest = meanest - min(self.x)
    #    print('estimates',meanest,sigest)
        popt, pcov = optimize.curve_fit(funcgauss,self.x,self.y,p0 = [min(self.y),max(self.y),meanest,sigest])
        print('-Gaussian fit results-')
    #    print('amplitude {}\nmean {}\nsigma {}'.format(*popt))
        print('y-shift {}\namplitude {}\nmean {}\nsigma {}'.format(*popt))

        print('covariance matrix \n{}'.format(pcov))
    #    print('pcov',pcov)
        return popt
        
    def SchPeak(self,show=True,xrange=[12,13],K=0.9,lambdaKa=0.15406):

        x1,x2=xrange
        'xseg and yseg:x and y segments of data in selected xrange'
        xseg,yseg = [],[]
        for n in self.x:
            if n >= x1 and  n <= x2:
                xseg.append(n)
                yseg.append(self.y[list(self.x).index(n)]) 
        
        
        y0,a,mean,sigma = Chart(self.x, self.y).gaussfit()
        ysegfit = funcgauss(np.array(xseg),y0,a,mean,sigma)
        
        'FULL WIDTH AT HALF MAXIMUM'
        FWHM_deg = sigma*2*np.sqrt(2*np.log(2))
        FWHM = FWHM_deg*np.pi/180
        print('\nFWHM == sigma*2*sqrt(2*ln(2)): {} degrees'.format(FWHM_deg))

        'scherrer width peak calculations'
        max_twotheta = xseg[list(yseg).index(max(yseg))]

        theta=max_twotheta/2
        theta=theta*np.pi/180

        print('K (shape factor): {}\nK-alpha: {} nm \nmax 2-theta: {} degrees'.\
            format(K,lambdaKa,max_twotheta))
        
        Sch=scherrer(K,lambdaKa,FWHM,theta)
        X,Y = xseg,ysegfit

        print('\nSCHERRER WIDTH: {} nm'.format(Sch))
        
        if show:
            plt.plot(xseg,yseg,color='m')

        return Sch,X,Y


    '''Function for an "n" point moving average: '''
    def mav(self,n=1,show=False):

        L=int(len(self.x)//n)
        newy=np.zeros(L)
        for i in range(L):
            k=0
            while k < n:
                newy[i] += self.y[(i*n)+k]
                k += 1
    #           print(i)
            newy[i]=newy[i]/n

        newx=np.zeros(L)
        for i in range(L):
            newx[i] = self.x[i*n]

        'update'
        self.x, self.y = newx,newy

        if show:
            plt.plot(self.x,self.y)

        return newx,newy


    '''Calculate relative peak intensity (i.e. comparing one peak to another)'''
    def XRD_int_ratio(self,xR1=[8.88,9.6],xR2=[10.81,11.52]):
        'XRD b/t two intensities ratio'
        return Chart(self.x, self.y).local_max(xR2)[1]/Chart(self.x, self.y).local_max(xR1)[1]



    def backsub(self,tol=1,show=False):
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
        
        L=len(self.y)
        lmda = int(0.50*L/(self.x[0]-self.x[L-1]))         #   'approx. # points for half width of peaks'

        backsub_y=np.zeros(L)
        for i in range(L):
            if self.y[(i+lmda)%L] > tol*self.y[i]:          #tolerance 'tol'
                backsub_y[(i+lmda)%L] = self.y[(i+lmda)%L] - self.y[i]
            else:
                if self.y[(i+lmda)%L] < self.y[i]:
                    backsub_y[(i+lmda)%L] = 0
        
        'update'
        self.x = self.x
        self.y = backsub_y

        if show:
            plt.plot(self.x,self.y)

        return self.x,backsub_y
    
    
