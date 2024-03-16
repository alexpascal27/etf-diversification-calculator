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
        self.wait_time = 10
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

    def _init_browser(self, etf_symbol):
        driver = webdriver.Firefox()
        driver.implicitly_wait(self.wait_time)
        url = "https://investengine.com/etfs/" + etf_symbol
        try:
            driver.get(url)
        except ec.WebDriverException:
            print("{} not retrieved (web driver error)\n".format(etf_symbol))
            driver.close()
            return None
        return driver


    def _get_to_starting_place(self, driver):
        driver.execute_script("window.scrollTo(0, {})".format(self.ETF_BREAKDOWN_STARTING_HEIGHT))

    def _scroll_down(self, driver):
        driver.execute_script("window.scrollBy(0, 500);")
        # time.sleep(2)  # Adjust the sleep time as necessary

    def _is_element_in_view(self, driver, elem):
        elem_left_bound = elem.location.get('x')
        elem_top_bound = elem.location.get('y')
        elem_width = elem.size.get('width')
        elem_height = elem.size.get('height')
        elem_right_bound = elem_left_bound + elem_width
        elem_lower_bound = elem_top_bound + elem_height

        win_upper_bound = driver.execute_script('return window.pageYOffset')
        win_left_bound = driver.execute_script('return window.pageXOffset')
        win_width = driver.execute_script('return document.documentElement.clientWidth')
        win_height = driver.execute_script('return document.documentElement.clientHeight')
        win_right_bound = win_left_bound + win_width
        win_lower_bound = win_upper_bound + win_height

        return all((win_left_bound <= elem_left_bound,
                    win_right_bound >= elem_right_bound,
                    win_upper_bound <= elem_top_bound,
                    win_lower_bound >= elem_lower_bound)
                   )

    def _at_end_of_page(self, driver):
        title_element = driver.find_element(By.XPATH, "//*[text()='Why InvestEngine']")
        return self._is_element_in_view(driver, title_element)

    def _get_etf_holdings(self, driver):
        holding_elements = driver.find_elements(By.XPATH,
                                                "//span[@class='Text_Text_lineHeightDesktop_16__KflzO "
                                                "Text_Text_lineHeightMobile_16__qTdTf "
                                                "Text_Text_sizeDesktop_14__RJHrm Text_Text_sizeMobile_14__TOFG7 "
                                                "Text_Text_overflowDesktop_ellipsis__2x2Mg "
                                                "Text_Text_overflowMobile_ellipsis__i35Ut']")

        return [element.text for element in holding_elements if element.text != ""]

    def _get_etf_from_investengine(self, etf_symbol):
        driver = self._init_browser(etf_symbol)
        etf_holdings = self._get_etf_holdings(driver)

        driver.quit()

    def generate_report(self):
        for symbol in self.etf_symbols:
            self._get_etf_from_investengine(symbol)


def main():
    downloader = ETFDiversificationCalculator()
    downloader.generate_report()


if __name__ == "__main__":
    main()
