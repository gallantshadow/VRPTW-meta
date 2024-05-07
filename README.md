# Project README

## Dependencies:
- pypy3

## Installation:
To install all the necessary packages for this project, ensure you have pypy3 installed. Then run the following command:
```bash
pypy3 -m pip install <package1> <package2> ... <packageN>
```
Replace `<package1>`, `<package2>`, etc., with the names of the necessary packages.

**Note:** If you decide to use python3 instead of pypy3, it's essential to keep the number of iterations below 10,000 in `main.py`. python3 run time will very high.

## How to run trials and change hyperparameters?
There is commented code in main.py for trials. It is commented because it takes 7 hours to run.
All changes from the dataset filename to hyperparameters can be made through main.py. Refer to the comments and documentation within main.py to understand how to modify these configurations.
