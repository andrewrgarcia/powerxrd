# powerxrd
Simple tools to handle powder XRD (and XRD) data



## Installation

```ruby
pip install powerxrd
```
## Usage Example

```ruby
import powerxrd as xrd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('/your-path-to-powerxrd/sample1.xy', sep='\t', header=None)  
x,y = np.array(df).T
x,y = xrd.backsub(x,y)

plt.plot(x,y)
plt.xlabel('2 $\\theta$')
```
![alt text](https://github.com/andrewrgarcia/powerxrd/blob/main/img/readme.png?raw=true)

## Contributors

- [Andrew Garcia](https://github.com/andrewrgarcia) - creator and maintainer

## Contributing

1. Fork it (<https://github.com/your-github-user/tensorscout/fork>)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

