# powerxrd
Simple tools to handle powder XRD (and XRD) data

## Installation

```bash
pip install powerxrd
```
## Usage
On your Terminal ("command line"), copy-paste the following lines:
```python 
cd Desktop   		# go to your Desktop
mkdir pxrd		# create a folder called pxrd

cd pxrd 		# go inside that folder
touch example.py  	# create example.py file
wget https://raw.githubusercontent.com/andrewrgarcia/powerxrd/main/sample1.xy	# download sample1.xy file
```

### Plots from tests/test_module

Code shows basic application of this module. On a blank Python file, type the following:


```python
import powerxrd as xrd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

```python
def test_backsub():
    
    df = pd.read_csv('sample1.xy', sep='\t', header=None)   #'https://www.statology.org/pandas-read-text-file/'
    x,y = np.array(df).T

    chart = xrd.Chart(x,y)

    chart.emission_lines(show=True)
    plt.plot(x,y,label='no backsub')
    plt.plot(*chart.backsub(),label='backsub')
    plt.xlabel('2 $\\theta$')
    plt.legend()
    plt.show()
```


```python
'''[OUT]
-Gaussian fit results-
y-shift 11692.125692754556
amplitude 2095353.5051754152
mean 33.62661656530919
sigma 15.966392102035668
covariance matrix 
[[ 8.46197862e+07 -6.62161996e+09 -2.35993662e+03 -2.92153344e+04]
 [-6.62161996e+09  5.72042049e+11  1.44541382e+05  2.60212877e+06]
 [-2.35993662e+03  1.44541382e+05  4.03327433e+00  3.38864534e-01]
 [-2.92153344e+04  2.60212877e+06  3.38864534e-01  1.46624777e+01]]

FWHM == sigma*2*sqrt(2*ln(2)): 37.597980168697426 degrees
K (shape factor): 0.9
K-alpha: 0.15406 nm 
max 2-theta: 19.91162984576907 degrees
Scherrer Width == K*lmda / (FWHM*cos(theta))

SCHERRER WIDTH: 0.2145261012981139 nm
'''
```
<img src="https://github.com/andrewrgarcia/powerxrd/blob/main/img/Figure_1.png?raw=true" width="500" >


```python
def test_sch():
    
    df = pd.read_csv('sample1.xy', sep='\t', header=None)   #'https://www.statology.org/pandas-read-text-file/'
    x,y = np.array(df).T

    chart = xrd.Chart(x,y)

    chart.backsub(tol=1.0,show=True)
    chart.SchPeak(show=True,xrange=[18,22])
    plt.xlabel('2 $\\theta$')
    plt.title('backsub and Scherrer width calculation')
    plt.show()
```

<img src="https://github.com/andrewrgarcia/powerxrd/blob/main/img/Figure_2.png?raw=true" width="500" >



```python
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
```

<img src="https://github.com/andrewrgarcia/powerxrd/blob/main/img/Figure_3.png?raw=true" width="500" >

## Contributors

- [Andrew Garcia](https://github.com/andrewrgarcia) - creator and maintainer

## Contributing

1. Fork it (<https://github.com/your-github-user/tensorscout/fork>)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

