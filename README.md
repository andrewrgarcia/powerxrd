# powerxrd
Simple tools to handle powder XRD (and XRD) data



## Installation

```bash
pip install powerxrd
```
## Usage Example
On your Terminal ("command line"), copy-paste the following lines:
```python 
cd Desktop   		# go to your Desktop
mkdir pxrd		# create a folder called pxrd

cd pxrd 		# go inside that folder
touch example.py  	# create example.py file
wget https://raw.githubusercontent.com/andrewrgarcia/powerxrd/main/sample1.xy	# download sample1.xy file
```

**example.py**:
```ruby
import powerxrd as xrd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('sample1.xy', sep='\t', header=None)  
x,y = np.array(df).T
x,y = xrd.backsub(x,y)

plt.plot(x,y)
plt.xlabel('2 $\\theta$')
plt.show()
```

Run the `example.py` file

![alt text](https://github.com/andrewrgarcia/powerxrd/blob/main/img/readme.png?raw=true)

## Contributors

- [Andrew Garcia](https://github.com/andrewrgarcia) - creator and maintainer

## Contributing

1. Fork it (<https://github.com/your-github-user/tensorscout/fork>)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

