# Description

Scrapes https://investengine.com/etfs/ for ETF holdings and looks for common shares. 
The more shares in common the higher the score. See `report.csv` for details.              

# How to use

`python3  etf_diversification_calc.py --symbols VWRP SPXP VHVG`

### Inspiration
https://github.com/PiperBatey/holdings_dl