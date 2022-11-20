import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize
import pandas


def braggs(twotheta,lmda=1.54):
    '''interplanar spacing "d_hkl" from Braggs law'''

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


def scherrer(K,lmda,beta,theta):
    '''Scherrer equation'''
    print('Scherrer Width == K*lmda / (FWHM*cos(theta))')
    return K*lmda / (beta*np.cos(theta))    #tau


def funcgauss(x,y0,a,mean,sigma):
    '''Gaussian equation'''
    return y0+(a/(sigma*np.sqrt(2*np.pi)))*np.exp(-(x-mean)**2/(2*sigma*sigma))


class Data:
    def __init__(self,file):
        '''Data structure.
        Parameters
        ----------
        file : str
            file name and/or path for XRD file in .xy format
        '''
        self.file = file

    
    def importfile(self):

        df = pandas.read_csv(self.file, sep='\t', header=None)   #'https://www.statology.org/pandas-read-text-file/'
        x,y = np.array(df).T

        return x,y

class Chart:

    def __init__(self,x,y):
        '''Chart structure. Constructs x-y XRD data to manipulate and analyze. 

        Parameters
        ----------
        x : np.array(float)
            array with x-data 2-theta values
        y : np.array(float)
            array with y-data peak intensity values
        K : float
            dimensionless shape factor for Scherrer equation (default 0.9)
        lambdaKa : float
            X-ray wavelength of \alpha radiation
        lambdaKi : float
            X-ray wavelength of "i" radiation (\beta, \gamma, other)
        '''
        self.x          = x          # x values
        self.y          = y          # y values
        self.K          = 0.9       
        self.lambdaKa   = 0.15406
        self.lambdaKi   = 0.139

    def local_max(self,xrange=[12,13]):
        '''Maximum finder in specified xrange

        Parameters
        ----------
        xrange_Ka : [](float)
            range of x to find globalmax
        '''

        i_l = self.x.searchsorted(xrange[0], 'left')
        i_r = self.x.searchsorted(xrange[1], 'right')

        'segments of x-y data within specified xrange'
        xseg = self.x[i_l:i_r]
        yseg = self.y[i_l:i_r]
        
        'find maximum y value within specified range and corresponding x loc.'
        imax = np.argmax(yseg)
        max_x = xseg[imax]
        max_y = yseg[imax]

        print('local_max -- max x: {} max y: {}'.format(max_x,max_y))
        return max_x, max_y

    def emission_lines(self, xrange_Ka=[10,20], show = True):
        '''Emission lines arising from different types of radiation i.e. K_beta radiation
        wavelength of K_beta == 0.139 nm
        
        Parameters
        ----------
        show: bool
            show plot of XRD chart
        xrange_Ka : [](float)
            range of x-axis (2-theta) for K_alpha radiation
        '''
        twothet_Ka_deg, int_Ka = Chart(self.x, self.y).local_max(xrange=xrange_Ka)
        twothet_Ka=twothet_Ka_deg*np.pi/180

        twothet_Ki = 2*np.arcsin((self.lambdaKi/self.lambdaKa)*np.sin(twothet_Ka/2))
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
        '''Fit of a Gaussian curve ("bell curve") to raw x-y data'''
        meanest = self.x[list(self.y).index(max(self.y))]
        sigest = meanest - min(self.x)
        popt, pcov = optimize.curve_fit(funcgauss,self.x,self.y,p0 = [min(self.y),max(self.y),meanest,sigest])
        print('\n-Gaussian fit results-')
        print('y-shift {}\namplitude {}\nmean {}\nsigma {}'.format(*popt))
        print('covariance matrix \n{}'.format(pcov))
        return popt

        
    def SchPeak(self,xrange=[12,13],show=True):
        '''Scherrer width calculation for peak within a specified range
        
        Parameters
        ----------
        xrange : [](float)
            range of x-axis (2-theta) where peak to be calculated is found
        show: bool
            show plot of XRD chart
        '''

        print('\nSchPeak: Scherrer width calc. for peak in range of [{},{}]'.format(*xrange))

        'xseg and yseg:x and y segments of data in selected xrange'
        xseg,yseg = [],[]
        for n, j in zip(self.x,self.y):
            if n >= xrange[0] and n <= xrange[1]:
                xseg.append(n)
                yseg.append(j) 

        
        y0,a,mean,sigma = Chart(xseg,yseg).gaussfit()
        ysegfit = funcgauss(np.array(xseg),y0,a,mean,sigma)

        'FULL WIDTH AT HALF MAXIMUM'
        FWHM_deg = sigma*2*np.sqrt(2*np.log(2))
        FWHM = FWHM_deg*np.pi/180
        print('\nFWHM == sigma*2*sqrt(2*ln(2)): {} degrees'.format(FWHM_deg))

        HWMIN = sigma*np.sqrt(2*np.log((50)))
        print('\nHalf-width Minimum (HWMIN) (1/50 max) == sigma*sqrt(2*ln(50)): {} degrees'.\
            format(HWMIN))

        'scherrer width peak calculations'
        max_x = xseg[list(yseg).index(max(yseg))]

        theta=max_x/2
        theta=theta*np.pi/180

        print('K (shape factor): {}\nK-alpha: {} nm \nmax 2-theta: {} degrees'.\
            format(self.K,self.lambdaKa,max_x))
        
        Sch=scherrer(self.K,self.lambdaKa,FWHM,theta)
        X,Y = xseg,ysegfit

        print('\nSCHERRER WIDTH: {} nm'.format(Sch))
        
        if show:
            plt.plot(X,Y,'c--')             # gauss fit 
            plt.plot(xseg,yseg,color='m')   # fitted segment

        left = mean - HWMIN
        right = mean + HWMIN 

        # return Sch,X,Y
        return max_x, max(yseg), Sch, left,right

    def allpeaks_recur(self,left=0, right=1, tols=(0.2,0.8),schpeaks=[],show = True):
        '''recursion component function for main allpeaks function below'''
        print('left right',left,right)
        maxx, maxy = Chart(self.x, self.y).local_max(xrange=[left,right])

        tol_h, dist_top = tols        

        Sch_x, Sch_y, Sch, l,r = Chart(self.x, self.y).SchPeak(xrange=[maxx-dist_top,maxx+dist_top],show=show)

        # self.schpeaks.append(Sch)
        schpeaks.append([Sch_x,Sch_y,Sch])
        peak_max = maxy

        if peak_max > tol_h*max(self.y):
            Chart(self.x, self.y).allpeaks_recur(r, right,tols,schpeaks,True)
            Chart(self.x, self.y).allpeaks_recur(left, l,tols,schpeaks,True)


    def allpeaks(self, tols=(0.2,0.8), show = True):
        '''Driver code for allpeaks recursion : Automated Scherrer width calculation of all peaks
        
        Parameters
        ----------
        tols : (float, float)
            tolerances for recursion 
            tol[0]: Minimum peak height to be calculated as a percent of maximum peak in chart (default=0.2 [20% of global maximum])
            tol[1]: Distance from top of peak to its tail (default=0.8)
        show: bool
            show plot of XRD chart
        '''

        #init xrange [left, right]
        left = min(self.x)
        right = max(self.x)
        schpeaks_ = []

        Chart(self.x, self.y).allpeaks_recur(left, right, tols, schpeaks_, True)


        print('\nallpeaks : Automated Scherrer width calculation of all peaks'+\
             ' [within a certain tolerance]\nSUMMARY:')
        print('2-theta / deg, \t Intensity, \t Sch width / nm')

        # for i in schpeaks_:
        #     print('2-theta: {} deg - Sch width: {} nm'.format(*i))

        sortidcs = np.argsort(np.array(schpeaks_).T[0])
        # print(sortidcs)
        for i in sortidcs:
            print('{}, \t  {}, \t  {} '.format(*schpeaks_[i]))





    def mav(self,n=1,show=False):
        '''Function for an "n" point moving average. '''
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


    def XRD_int_ratio(self,xR1=[8.88,9.6],xR2=[10.81,11.52]):
        '''Calculate relative peak intensity (i.e. comparing one peak to another)'''
        # 'XRD b/t two intensities ratio'
        return Chart(self.x, self.y).local_max(xR2)[1]/Chart(self.x, self.y).local_max(xR1)[1]



    def backsub(self,tol=1,show=False):
        '''Background subtraction operation
        inputs:
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