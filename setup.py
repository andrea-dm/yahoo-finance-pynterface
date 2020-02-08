import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yahoo_finance_pynterface",
    version="1.0.4",
    author="Andrea del Monaco",
    author_email="and.delmonaco@gmail.com",
    description="A Python Interface to the Yahoo Finance API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrea-dm/yahoo-finance-pynterface",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",
    ],
    install_requires=[
        'requests >= 2.19.1',
        'pandas >= 0.23.4',
        'numpy >= 1.15.1',
        'pytz >= 2018.5',
        'aenum >= 2.1.2',
    ],
)
