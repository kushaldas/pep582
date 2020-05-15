## Single file PEP582 implementation




This is a single file implementation for [PEP 582](https://www.python.org/dev/peps/pep-0582/).

## How to use?


```
curl https://raw.githubusercontent.com/kushaldas/pep582/master/pep582.py -o pep582.py
python3 pep582.py --install
```

Now, inside of any directory, if you create  another directory called `__pypackages__`, `python3`
will start using it to install any modules via `pip` and also use those modules (if you are in the same directory).

```
python3 -m pip install requests
```

This command will then install the `request` module in `__pypackages__`.

