#!/usr/bin/env python3

# This is a small single file tool to implement PEP 582 as an external hack.
# Read https://www.python.org/dev/peps/pep-0582/ for more details.

import os
import sys
import site
import argparse

def install():
    "To install in the users site-packaes directory"

    site_path = os.path.join(site.getusersitepackages(), "pep582.py")
    data = ""
    with open(__file__) as fobj:
        data = fobj.read()

    with open(site_path, "w") as fobj:
        fobj.write(data)

    print(f"Successfully installed in {site_path}")


def main():
    """The main entry point.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true",
                    help="Install the tool to users' site-packages directory")
    args = parser.parse_args()

    if args.install:
        install()


if __name__ == "__main__":
    main()
