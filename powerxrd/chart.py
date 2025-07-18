import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize

from .utilities import funcgauss, scherrer, braggs

class Chart:

    def __init__(self,x,y):
        '''
        Chart structure. Constructs x-y XRD data to manipulate and analyze. 

        Parameters
        ----------
        x : np.array(float)
            array with x-data 2-theta values
        y : np.array(float)
            array with y-data peak intensity values
        K : float
            dimensionless shape factor for Scherrer equation (default 0.9)
        lambdaKa : float
            X-ray wavelength of alpha radiation
        lambdaKi : float
            X-ray wavelength of "i" radiation (beta, gamma, other)
        '''
        self.x          = x          # x values
        self.y          = y          # y values
        self.K          = 0.9       
        self.lambdaKa   = 0.15406
        self.lambdaKi   = 0.139
        self.background_points = None  # New attribute to store background points

    def set_background_points(self, background_points):
        self.background_points = background_points

    def interpolate_background(self):
        if self.background_points is not None:
            # Implement your chosen interpolation method here
            # For example, using numpy's interpolation functions:
            x_bg_points, y_bg_points = zip(*self.background_points)
            interpolated_bg = np.interp(self.x, x_bg_points, y_bg_points)
            self.y -= interpolated_bg  # Subtract the interpolated background from the y data


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


    def gaussfit(self, verbose=True):
        '''Fit of a Gaussian curve ("bell curve") to raw x-y data'''
        meanest = self.x[list(self.y).index(max(self.y))]
        sigest = meanest - min(self.x)
        popt, pcov = optimize.curve_fit(
            funcgauss, self.x, self.y,
            p0=[min(self.y), max(self.y), meanest, sigest],
            maxfev=5000  # Prevent early failure
        )

        if verbose:
            print('\n-Gaussian fit results-')
            print('y-shift {}\namplitude {}\nmean {}\nsigma {}'.format(*popt))
            print('covariance matrix \n{}'.format(pcov))
        return popt

        
    def SchPeak(self,xrange=[12,13],verbose=True, show=True):
        '''Scherrer width calculation for peak within a specified range
        
        Parameters
        ----------
        xrange : [](float)
            range of x-axis (2-theta) where peak to be calculated is found
        show: bool
            show plot of XRD chart
        '''

        # print('\nSchPeak: Scherrer width calc. for peak in range of [{},{}]'.format(*xrange))

        'xseg and yseg:x and y segments of data in selected xrange'
        xseg,yseg = [],[]
        for n, j in zip(self.x,self.y):
            if n >= xrange[0] and n <= xrange[1]:
                xseg.append(n)
                yseg.append(j) 

        
        y0,a,mean,sigma = Chart(xseg,yseg).gaussfit(verbose)
        ysegfit = funcgauss(np.array(xseg),y0,a,mean,sigma)

        'FULL WIDTH AT HALF MAXIMUM'
        FWHM_deg = sigma*2*np.sqrt(2*np.log(2))
        FWHM = FWHM_deg*np.pi/180
        # print('\nFWHM == sigma*2*sqrt(2*ln(2)): {} degrees'.format(FWHM_deg))

        # Store FWHM as attribute // user request :: hnmachado github issue/8
        self.FWHM_deg = FWHM_deg
        self.FWHM_rad = FWHM

        HWMIN = sigma*np.sqrt(2*np.log((50)))
        # print('\nHalf-width Minimum (HWMIN) (1/50 max) == sigma*sqrt(2*ln(50)): {} degrees'.\
        #     format(HWMIN))

        'scherrer width peak calculations'
        max_x = xseg[list(yseg).index(max(yseg))]

        theta=max_x/2
        theta=theta*np.pi/180

        # print('K (shape factor): {}\nK-alpha: {} nm \nmax 2-theta: {} degrees'.\
        #     format(self.K,self.lambdaKa,max_x))
        
        Sch=scherrer(self.K,self.lambdaKa,FWHM,theta)
        X,Y = xseg,ysegfit

        # print('\nSCHERRER WIDTH: {} nm'.format(Sch))

        if verbose:
            print('\nSchPeak: Scherrer width calc. for peak in range of [{},{}]'.\
                                    format(*xrange))
            print('\nFWHM == sigma*2*sqrt(2*ln(2)): {} degrees'.\
                                    format(FWHM_deg))
            print('K (shape factor): {}\nK-alpha: {} nm \nmax 2-theta: {} degrees'.\
                                    format(self.K,self.lambdaKa,max_x))
            print('\nSCHERRER WIDTH: {} nm'.\
                                    format(Sch))

        
        if show:
            plt.plot(X,Y,'c--')             # gauss fit 
            plt.plot(xseg,yseg,color='m')   # fitted segment

        left = mean - HWMIN
        right = mean + HWMIN 

        # return Sch,X,Y
        return max_x, max(yseg), Sch, left,right





    def allpeaks_recur(self,left=0, right=1, tols_=(2e5,0.8),schpeaks=[],verbose = False, show = True):
        '''recursion component function for main allpeaks function below'''
        # print('left right',left,right)
        max_x, max_y = Chart(self.x, self.y).local_max(xrange=[left,right])
        maxpeak_height, peaktrough_d = tols_ 
        peak_max = max_y     

        if peak_max > maxpeak_height:
            xrange = [ max_x - peaktrough_d, max_x + peaktrough_d ]
            Sch_x, Sch_y, Sch, l,r = Chart(self.x, self.y).\
                        SchPeak(xrange,verbose,show)
            schpeaks.append([Sch_x,Sch_y,Sch])

            Chart(self.x, self.y).allpeaks_recur(left, l,tols_,schpeaks,verbose,show)
            Chart(self.x, self.y).allpeaks_recur(r, right,tols_,schpeaks,verbose,show)


    def allpeaks(self, tols=(0.2,0.8), verbose=False, show = True):
        '''Driver code for allpeaks recursion : Automated Scherrer width calculation of all peaks
        
        Parameters
        ----------
        tols : (float, float)
            tolerances for recursion 
            tol[0]: Minimum peak height to be calculated as a percent of the chart's global maximum (default=0.2 [20% of global maximum])
            tol[1]: Average distance from peak (top) to trough (bottom) of all peak (default=0.8)
        show: bool
            show plot of XRD chart
        '''
        print('\n-------------------------------------------\nALLPEAKS: '+\
            'Automated Scherrer width calculations with a recursive search of local maxima\n')

        #init xrange [left, right]
        left = min(self.x)
        right = max(self.x)
        schpeaks_ = []

        max_x, max_y = Chart(self.x, self.y).local_max(xrange=[left,right])
        print('\n')
        maxpeak_height = max_y*tols[0]
        peaktrough_d = tols[1]

        tols_ = (maxpeak_height, peaktrough_d)
        Chart(self.x, self.y).allpeaks_recur(left, right, tols_, schpeaks_,verbose,show)


        print('\nSUMMARY (.csv format):')
        print('2-theta / deg, \t Intensity, \t Sch width / nm')

        # for i in schpeaks_:
        #     print('2-theta: {} deg - Sch width: {} nm'.format(*i))

        sortidcs = np.argsort(np.array(schpeaks_).T[0])
        # print(sortidcs)
        for i in sortidcs:
            print('{}, \t  {}, \t  {} '.format(*schpeaks_[i]))


    def XRD_int_ratio(self,xR1=[8.88,9.6],xR2=[10.81,11.52]):
        '''Calculate relative peak intensity (i.e. comparing one peak to another)'''
        # 'XRD b/t two intensities ratio'
        return Chart(self.x, self.y).local_max(xR2)[1]/Chart(self.x, self.y).local_max(xR1)[1]


    def mav(self, n=1, inplace=False, show=False, return_x=True):
        """
        Apply an `n`-point moving average to the XRD data.

        Parameters
        ----------
        n : int, optional
            Number of points to average over (window size). Must be >= 1. Default is 1.
        inplace : bool, optional
            If True, update self.x and self.y with the smoothed data. Default is False.
        show : bool, optional
            If True, display the smoothed data using matplotlib.
        return_x : bool, optional
            If False, only return the smoothed y-data. Useful for post-processing. Default is True.

        Returns
        -------
        tuple or ndarray or Chart
            Returns (newx, newy) if inplace is False and return_x is True,
            newy if return_x is False,
            or self if inplace is True.
        """
        if n < 1:
            raise ValueError("n must be >= 1 for a moving average.")

        # Use convolution for efficiency
        kernel = np.ones(n) / n
        newy = np.convolve(self.y, kernel, mode='valid')

        # Match x length (drop n//2 points from start and end)
        newx = self.x[:len(newy)]  # Simplified assumption: evenly spaced

        if show:
            plt.plot(newx, newy)
            plt.title(f"{n}-point Moving Average")
            plt.xlabel("2θ (deg)")
            plt.ylabel("Intensity")

        if inplace:
            self.x, self.y = newx, newy
            return self
        else:
            if return_x:
                return newx, newy
            else:
                return newy



    def backsub(self, tol=1, inplace=False, show=False):
        """
        Perform a simple tolerance-based background subtraction.

        This algorithm subtracts local minima based on a rolling comparison with a forward-offset window,
        zeroing out data points that fall below a tolerance threshold.

        Parameters
        ----------
        tol : float, optional
            Tolerance threshold. Background is subtracted if a forward intensity exceeds the current
            point by more than `tol` times. Default is 1.
        inplace : bool, optional
            If True, modifies self.y in-place. Default is False.
        show : bool, optional
            If True, plot the resulting background-subtracted data.

        Returns
        -------
        tuple or Chart
            (self.x, backsub_y) if inplace is False, otherwise returns self.
        """

        L=len(self.y)
        # Approximate half-width in index space (reverse-sorted check)
        lmda = int(0.50*L/(self.x[0]-self.x[L-1]))         

        backsub_y=np.zeros(L)
        for i in range(L):
            if self.y[(i+lmda)%L] > tol*self.y[i]:          #tolerance 'tol'
                backsub_y[(i+lmda)%L] = self.y[(i+lmda)%L] - self.y[i]
            else:
                if self.y[(i+lmda)%L] < self.y[i]:
                    backsub_y[(i+lmda)%L] = 0
        
        if show:
            plt.plot(self.x,self.y)

        'update'
        if inplace:
            self.y = backsub_y
            return self
        else:
            return self.x, backsub_y