import argparse
import math
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

'''
    File name: etf_diversification_calc.py
    Author: Alex Pascal
    Date created: 16/03/2024
    Date last modified: 9/3/2021
    Python Version: 3.11.4
    Description: InvestEngine ETF holding scraper generating a score and report.csv file
'''


class ETFDiversificationCalculator:
    ETF_BREAKDOWN_STARTING_HEIGHT = 1550

    def __init__(self):
        # variables
        self.etf_symbols = []
        self.wait_time = 15
        # init
        self._parse_command_args()

    def _parse_command_args(self):
        parser = argparse.ArgumentParser(
            formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=27))  # type error is ok

        title_group = parser.add_argument_group(title="required arguments")  # required arguments header in output
        input_type_group = title_group.add_mutually_exclusive_group(required=True)
        input_type_group.add_argument("--symbols", nargs='+', metavar="SYM", help="specify one or more ETF symbols")
        args = parser.parse_args()
        if args.symbols:
            self.etf_symbols = args.symbols

    def _get_to_starting_place(self, driver):
        driver.execute_script("window.scrollTo(0, {}})".format(self.ETF_BREAKDOWN_STARTING_HEIGHT))

    def _get_etf_from_investengine(self, etf_symbol):
        driver = webdriver.Firefox()
        driver.implicitly_wait(self.wait_time)
        wait = WebDriverWait(driver, 30, poll_frequency=1)
        url = "https://investengine.com/etfs/" + etf_symbol
        try:
            driver.get(url)
        except ec.WebDriverException:
            print("{} not retrieved (web driver error)\n".format(etf_symbol))
            driver.close()
            return False

        wait.until(self._get_to_starting_place)
        # TODO: add the below back in
        #  driver.quit()

    def generate_report(self):
        for symbol in self.etf_symbols:
            self._get_etf_from_investengine(symbol)


def main():
    downloader = ETFDiversificationCalculator()
    downloader.generate_report()


if __name__ == "__main__":
    main()
