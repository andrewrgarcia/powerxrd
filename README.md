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
    
    data = xrd.Data('sample1.xy').importfile()
    chart = xrd.Chart(*data)

    chart.emission_lines(show=True)
    plt.plot(*data,label='no backsub')
    plt.plot(*chart.backsub(),label='backsub')
    plt.xlabel('2 $\\theta$')
    plt.legend()
    plt.show()
```

<img src="https://github.com/andrewrgarcia/powerxrd/blob/main/img/Figure_1.png?raw=true" width="500" >

```python
def test_sch():
    
    data = xrd.Data('sample1.xy').importfile()
    chart = xrd.Chart(*data)

    chart.backsub(tol=1.0,show=True)
    chart.SchPeak(show=True,xrange=[18,22])
    plt.xlabel('2 $\\theta$')
    plt.title('backsub and Scherrer width calculation')
    plt.show()
```
```python
'''[OUT]
SchPeak: Scherrer width calc. for peak in range of [18,22]

-Gaussian fit results-
y-shift 10071.343657500349
amplitude 498186.5044519722
mean 19.921493157135924
sigma 0.1692913723155234
covariance matrix 
[[ 2.20553363e+07 -1.98537382e+07 -3.73304414e-08 -4.49772395e+00]
 [-1.98537382e+07  7.90011550e+07 -2.89541102e-09  1.78971558e+01]
 [-3.73304414e-08 -2.89541102e-09  9.41177383e-06 -8.26802823e-12]
 [-4.49772395e+00  1.78971558e+01 -8.26802823e-12  1.03289908e-05]]

FWHM == sigma*2*sqrt(2*ln(2)): 0.39865071697939203 degrees
K (shape factor): 0.9
K-alpha: 0.15406 nm 
max 2-theta: 19.91162984576907 degrees
Scherrer Width == K*lmda / (FWHM*cos(theta))

SCHERRER WIDTH: 20.23261907915097 nm
'''
```
<img src="https://github.com/andrewrgarcia/powerxrd/blob/main/img/Figure_2.png?raw=true" width="500" >


```python
def test_mav():
    
    data = xrd.Data('sample1.xy').importfile()
    chart = xrd.Chart(*data)

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

