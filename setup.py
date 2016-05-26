""" Setup script
"""


import setuptools


DISTRIBUTION = 'pmpc'

VERSION = '0.0.0'

AUTHOR = 'sinoroc'

INSTALL_REQUIREMENTS = [
    'pypiwin32',
    'python-mpd2',
]

ENTRY_POINTS = {
    'console_scripts': [
        'pmpc = pmpc.script:main',
    ]
}

SETUP_REQUIREMENTS = [
    'pytest-runner',
    'setuptools-pep8',
    'setuptools-lint',
]

TEST_REQUIREMENTS = [
    'pytest',
]

PACKAGES_EXCLUDE = [
    'tests',
]
PACKAGES = setuptools.find_packages(exclude=PACKAGES_EXCLUDE)


setuptools.setup(
    name=DISTRIBUTION,
    version=VERSION,
    author=AUTHOR,
    packages=PACKAGES,
    entry_points=ENTRY_POINTS,
    install_requires=INSTALL_REQUIREMENTS,
    setup_requires=SETUP_REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
)


# EOF
