from setuptools import setup

setup(
    name='APCLI',
    version='0.1',
    py_modules=['ap'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        ap=ap:cli
    ''',
)
