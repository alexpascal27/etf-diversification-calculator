# ETF Diversity Calculator

> A simple Python script that evaluates share overlap within ETFs and calculates % similarity for each ETF comparison based on the number of common shares.

- [Dependencies](#dependencies)
- [Description](#description)
- [**How to Use**](#how-to-use)
  * [InvestEngine](#investengine)
    + [Simple Example](#simple-example)
  + [Cbonds](#cbonds)
    + [Simple Example](#simple-example-1)
  * [Both](#both)
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
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

# Description

Scrapes [InvestEngine](https://investengine.com/) and/or [Cbonds](https://cbonds.com/etf/) for ETF holdings and looks for common shares. 
The more shares in common the higher the % similarity. See `comparison.xlsx` for details.              

# Dependencies


## How to use
### InvestEngine
Go to https://investengine.com/etfs. Search for your etf and open it. Copy the `{broker}/{etf-symbol}` part of the URL following https://investengine.com/etfs/.
#### Simple Example
E.g. for 
1. https://investengine.com/etfs/vanguard/vhvg/?back=%2Fetfs%2Fcollections%2Fleading-global-indices%2F%3Fback%3D%252Fetfs%252F you want to use `vanguard/vhvg`
2. https://investengine.com/etfs/vanguard/vuag/?back=%2Fetfs%2Fcollections%2Fleading-global-indices%2F%3Fback%3D%252Fetfs%252F you want to use `vanguard/vuag`
3. https://investengine.com/etfs/invesco/spxp/?back=%2Fetfs%2Fcollections%2Fleading-global-indices%2F%3Fback%3D%252Fetfs%252F you want to use `invesco/spxp`
Then run the script with the symbols as arguments. E.g. 

`python3  etf_diversification_calc.py --investengine_symbols vanguard/vhvg vanguard/vuag invesco/spxp` and you get a comparison.xlsx file with the results.
A sheet for each 1-to-1 comparison.

### Cbonds
Go to https://cbonds.com/etf/. Search for your etf and open it. **MAKE SURE THE ETF PAGE HAS A STRUCTURE TABLE WITH HOLDINGS OTHERWISE THIS WON'T WORK** Copy the `{etf_id}` part of the URL following https://cbonds.com/etf/.
#### Simple Example
E.g. for https://cbonds.com/etf/3971/ you want to use `3971`
Then run the script with the symbols as arguments. E.g. 
`python3  etf_diversification_calc.py --cbonds_symbols 3971 9417` and you get a comparison.xlsx file with the results.
A sheet for each 1-to-1 comparison.

### Both

You can also use both sources at the same time. E.g.
`python3  etf_diversification_calc.py --investengine_symbols vanguard/vhvg vanguard/vuag invesco/spxp --cbonds_symbols 3971` and the comparison should be somwhat accurate. (It's more accurate if you use one source only, as they have different names for the same holding)

## Resources
All data comes from InvestEngine and/or Cbonds via [Selenium](https://selenium-python.readthedocs.io/)

## Author
* **Alex Pascal** (https://github.com/alexpascal27)

## Inspiration
https://github.com/PiperBatey/holdings_dl

## License

MIT License (see LICENSE file)
