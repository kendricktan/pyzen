# pyzen
Python API for the ZenCash daemon.
Only supports Python 3.x

# Installation
```
pip install git+https://github.com/kendricktan/pyzen.git@v1.0.0
```

# Example usage
* Make sure your zen daemon is running *

For help setting up ZenCash daemon refer to [this guide](https://github.com/zcash/zcash/wiki/1.0-User-Guide), **just replace zcashd with zend**. You can get zend [here](https://github.com/ZencashOfficial/zen/releases)

```python
from pyzen import PyZen

z = PyZen(host="127.0.0.1", port="8231",
          usename="RPC_USERNAME", password="RPC_PASSWORD")
z.getinfo()

# Should print out something similar
# {'version': 2000953, 'protocolversion': 170002, 'walletversion': 60000, 'balance': 79.81897094, 'blocks': 137309, 'timeoffset': 0, 'connections': 8, 'proxy': '', 'difficulty': 110596.1266266895, 'testnet': False, 'keypoololdest': 1499550931, 'keypoolsize': 101, 'paytxfee': 0.0, 'relayfee': 1e-06, 'errors': ''}
```

For a complete list of functions, refer to [the source code](https://github.com/kendricktan/pyzen/blob/master/pyzen/__init__.py)