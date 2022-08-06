#!/usr/bin/env python3

# This is a small single file tool to implement PEP 582 as an external hack.
# Read https://www.python.org/dev/peps/pep-0582/ for more details.

import os
import sys
import site
import argparse
import sysconfig

# Because a Fedora patch breaks it otherwise
# https://github.com/python/cpython/compare/3.10...fedora-python:cpython:fedora-3.10#diff-d593bd299ba58e440ba411ffa0640ccd9d20d518b0cf2644ed4bdb75a82a3e70R61
cpython_posix_prefix =  {
        'stdlib': '{installed_base}/{platlibdir}/python{py_version_short}',
        'platstdlib': '{platbase}/{platlibdir}/python{py_version_short}',
        'purelib': '{base}/lib/python{py_version_short}/site-packages',
        'platlib': '{platbase}/{platlibdir}/python{py_version_short}/site-packages',
        'include':
            '{installed_base}/include/python{py_version_short}{abiflags}',
        'platinclude':
            '{installed_platbase}/include/python{py_version_short}{abiflags}',
        'scripts': '{base}/bin',
        'data': '{base}',
        }

def install():
    """To install in the users site-packaes directory."""

    site_path = os.path.join(site.getusersitepackages(), "pep582.py")
    site_pth = os.path.join(site.getusersitepackages(), "pep582.pth")
    data = ""
    with open(__file__) as fobj:
        data = fobj.read()

    try:
        os.makedirs(site.getusersitepackages())
    except FileExistsError:
        # This means we already have the directory in place
        pass

    with open(site_path, "w") as fobj:
        fobj.write(data)

    with open(site_pth, "w") as fobj:
        fobj.write("import pep582;pep582.enable_local_pypackages()\n")

    print(f"Successfully installed in {site_path}")
    print(f"\nTo uninstall pep582:\n{sys.executable} -m pep582 --uninstall")


def uninstall():
    """To uninstall from the users site-packages directory"""

    site_packages = site.getusersitepackages()
    site_path = os.path.join(site_packages, "pep582.py")
    site_pth = os.path.join(site_packages, "pep582.pth")

    if not os.path.exists(site_path) and not os.path.exists(site_pth):
        print(f"pep582.py not found in {site_packages}")
        return

    if os.path.exists(site_path):
        os.remove(site_path)

    if os.path.exists(site_pth):
        os.remove(site_pth)

    print(f"Successfully uninstalled from {site_packages}")


def enable_magic(pypackages_path: str):
    """Enables our __pypackages__ if it exists, also tells pip where to install."""
    major = sys.version_info.major
    minor = sys.version_info.minor
    libname = "lib"
    if sys.implementation.name == "cpython":
        pname = "python"
    elif sys.implementation.name == "pypy":
        pname = "pypy"
    else:
        raise(OSError("Your Python implementation is not supported yet. Talk to Kushal."))
    # On Windows the spelling is capital Lib inside of the PIP_PREFIX
    if os.name == "nt":
        libname = "Lib"
    if os.path.exists(pypackages_path):
        os.environ["VIRTUAL_ENV"] = pypackages_path
        site_packages_path = os.path.join(
            pypackages_path, libname, f"{pname}{major}.{minor}", "site-packages"
        )
        if os.name == "nt":
            site_packages_path = os.path.join(
                pypackages_path, libname, "site-packages"
            )
        else:
            # We need this thanks to the Fedora's patch mentioned above.
            if sys.implementation.name == "cpython":
                sysconfig._INSTALL_SCHEMES["posix_prefix"] = cpython_posix_prefix
        sys.path.insert(0, site_packages_path)
        if sys.argv[0] == "-m":
            # let us try to fix pip here
            os.environ["PIP_PREFIX"] = pypackages_path


def enable_local_pypackages():
    """Function to use local __pypackages__ if not running via a script."""
    pwd = os.getcwd()
    if sys.argv[0] == "" or sys.argv[0] == "-m":  # Means python3
        pypackages_path = os.path.join(pwd, "__pypackages__")
        # check for the existance
        enable_magic(pypackages_path)
    else:
        basedir = os.path.dirname(sys.argv[0])
        pypackages_path = os.path.join(basedir, "__pypackages__")
        # check for the existance
        enable_magic(pypackages_path)


def main():
    """The main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install the tool to users' site-packages directory",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Uninnstall the tool from users' site-packages directory",
    )

    args = parser.parse_args()

    if args.install:
        install()
    elif args.uninstall:
        uninstall()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
