## Single file PEP582 implementation

This is a single file implementation for [PEP 582](https://www.python.org/dev/peps/pep-0582/).

Here is a demo on Windows

![Working on Windows](https://kushaldas.in/images/pep582_windows1.gif)

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

This command will then install the `requests` module in `__pypackages__`.


## What about executables installed via the modules?

The current implementation only supports running things via `python3 -m
modulename` if you are in the parent directory of the `__pypackages__`. 

