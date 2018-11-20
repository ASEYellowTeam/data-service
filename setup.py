import os
import sys
from distutils.sysconfig import get_python_lib

from setuptools import find_packages, setup

# CHANGE THIS -----
REPO_NAME = "data-service"
MODULE_NAME = "dataservice"
# -----------------

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    # noinspection PyStringFormat
    sys.stderr.write("""
==========================
Unsupported Python version
==========================

This version of Django requires Python {}.{}, but you're trying to
install it on Python {}.{}.

This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:

    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install django

This will install the latest version of Django which works on your
version of Python. If you can't upgrade your pip (or Python), request
an older version of Django:

    $ python -m pip install "django<2"
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


# Warn if we are installing over top of an existing installation. This can
# cause issues where files that were deleted from a more recent Django are
# still present in site-packages. See #18115.
overlay_warning = False
if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib/"):
        # We have to try also with an explicit prefix of /usr/local in order to
        # catch Debian's custom user site-packages directory.
        lib_paths.append(get_python_lib(prefix="/usr/local"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, "django"))
        if os.path.exists(existing_path):
            # We note the need for the warning here, but present it after the
            # command is run, so it's more likely to be seen.
            overlay_warning = True
            break


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


with open('requirements.txt') as fp:
    install_requires = fp.read()


setup(
    name=MODULE_NAME,
    version="0.2",
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    url='https://github.com/ytbeepbeep/'+REPO_NAME,
    author='Yellow Team',
    author_email='ytbeepbeep@gmail.com',
    description='Send reports via mail',
    long_description=read('README.md'),
    license='AGPL-3.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'dev': ['pytest', 'pytest-cov']
    },
    classifiers=[
        'License :: AGPL-3.0 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
    project_urls={
        'Source': 'https://github.com/ytbeepbeep/'+REPO_NAME,
    },
)


if overlay_warning:
    sys.stderr.write("""
========
WARNING!
========

You have just installed Django over top of an existing
installation, without removing it first. Because of this,
your install may now include extraneous files from a
previous version that have since been removed from
Django. This is known to cause a variety of problems. You
should manually remove the

%(existing_path)s

directory and re-install Django.

""" % {"existing_path": existing_path})
