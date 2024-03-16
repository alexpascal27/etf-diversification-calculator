# ETF Diversity Calculator

> A simple Python script that evaluates share overlap within ETFs and calculates a portfolio score based on the number of common shares.

- [Dependencies](#dependencies)
- [Description](#description)
- [**How to Use**](#how-to-use)
  * [Simple Example](#simple-example)
- [Resources](#resources)
- [Author](#author)
- [Inspiration](#inspiration)
- [License](#license)

## Dependencies
`pip install` the following:
* [Python 3](https://www.python.org/) (tested on 3.11)
* [Pandas](https://pandas.pydata.org/)
  * [NumPy](https://numpy.org/)
* [Selenium](https://selenium-python.readthedocs.io/)
* [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)

# Description

Scrapes https://investengine.com/etfs/ for ETF holdings and looks for common shares. 
The more shares in common the lower the diversification score. See `comparison.xlsx` for details.              

# Dependencies


## How to use
Go to https://investengine.com/etfs. Search for your etf and open it. Copy the `/{broker}/{etf-symbol}` part of the URL following https://investengine.com/etfs. 
### Simple Example
E.g. for 
1. https://investengine.com/etfs/vanguard/vhvg/?back=%2Fetfs%2Fcollections%2Fleading-global-indices%2F%3Fback%3D%252Fetfs%252F you want to use `vanguard/vhvg`
2. https://investengine.com/etfs/vanguard/vuag/?back=%2Fetfs%2Fcollections%2Fleading-global-indices%2F%3Fback%3D%252Fetfs%252F you want to use `vanguard/vuag`
3. https://investengine.com/etfs/invesco/spxp/?back=%2Fetfs%2Fcollections%2Fleading-global-indices%2F%3Fback%3D%252Fetfs%252F you want to use `invesco/spxp`
Then run the script with the symbols as arguments. E.g. 

`python3  etf_diversification_calc.py --symbols vanguard/vhvg vanguard/vuag invesco/spxp` and you get a comparison.xlsx file with the results.
A sheet for each 1-to-1 comparison and a summary sheet with scores.

## Resources
All data comes from InvestEngine view [Selenium](https://selenium-python.readthedocs.io/)

## Author
* **Alex Pascal** (https://github.com/alexpascal27)

## Inspiration
https://github.com/PiperBatey/holdings_dl

## License

MIT License (see LICENSE file)