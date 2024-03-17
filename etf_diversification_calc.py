import argparse
import statistics
import itertools
from enum import Enum
import re
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

'''
    File name: etf_diversification_calc.py
    Author: Alex Pascal
    Date created: 16/03/2024
    Date last modified: 17/03/2024
    Python Version: 3.11.4
    Description: ETF holding scraper generating a score and comparison.xlsx file
'''


class Share:
    def __init__(self, name: str, etf_name: str, percentage_of_etf: float):
        self.name = name
        self.etf_name = etf_name
        self.percentage_of_etf = percentage_of_etf


class ETF:
    def __init__(self, name: str, shares: list[Share]):
        self.name = name
        self.shares = shares


class Comparison:
    def __init__(self, etf1: list[Share], etf2: list[Share]):
        self.etf1 = etf1
        self.etf2 = etf2
        self.common_shares = self._get_common_shares(etf1, etf2)
        self.etf1_perc = 100 * len(self.common_shares) / len(etf1)
        self.etf2_perc = 100 * len(self.common_shares) / len(etf2)

    @staticmethod
    def _get_common_shares(etf1: list[Share], etf2: list[Share]) -> list[Share]:
        common_shares = []
        for share in etf1:
            for otherShare in etf2:
                if share.name == otherShare.name:
                    common_shares.append(
                        Share(share.name, share.etf_name + ' AND ' + otherShare.etf_name,
                              statistics.mean([share.percentage_of_etf, otherShare.percentage_of_etf])))
                    break
        return common_shares


class Platform(str, Enum):
    INVESTENGINE = 'investengine'
    CBONDS = 'cbonds'


class ETFDiversificationCalculator:
    ETF_BREAKDOWN_STARTING_HEIGHT = 1550
    FILE_PATH = "comparison.xlsx"

    def __init__(self):
        # variables
        self.platform: Platform = Platform.INVESTENGINE
        self.investengine_etf_symbols: list[str] = []
        self.cbonds_etf_symbols: list[str] = []
        self.wait_time: int = 20
        # init
        self._parse_command_args()

    def _parse_command_args(self):
        parser = argparse.ArgumentParser(
            formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=27))  # type error is ok

        title_group = parser.add_argument_group(title="required arguments")  # required arguments header in output
        title_group.add_argument("--cbonds_symbols", nargs='+', metavar="CBONDS_SYM",
                                 help="specify one or more cbonds ETF symbols",
                                 required=False)
        title_group.add_argument("--investengine_symbols", nargs='+', metavar="SYM", help="specify one or more ETF symbols",
                                 required=False)
        args = parser.parse_args()
        if args.cbonds_symbols:
            self.cbonds_etf_symbols = args.cbonds_symbols
        if args.investengine_symbols:
            self.investengine_etf_symbols = args.investengine_symbols

    def _init_browser(self, etf_symbol, platform) -> webdriver:
        driver = webdriver.Firefox()
        driver.implicitly_wait(self.wait_time)
        url = (("https://investengine.com/etfs/" if platform == Platform.INVESTENGINE else "https://cbonds.com/etf/")
               + etf_symbol)
        try:
            driver.get(url)
        except ec.WebDriverException:
            print("{} not retrieved (web driver error)\n".format(etf_symbol))
            driver.close()
            return None
        return driver

    def _get_name_list(self, driver) -> list[str]:
        holding_name_elements = driver.find_elements(By.XPATH,
                                                     "//span[@class='Text_Text_lineHeightDesktop_16__KflzO "
                                                     "Text_Text_lineHeightMobile_16__qTdTf "
                                                     "Text_Text_sizeDesktop_14__RJHrm Text_Text_sizeMobile_14__TOFG7 "
                                                     "Text_Text_overflowDesktop_ellipsis__2x2Mg "
                                                     "Text_Text_overflowMobile_ellipsis__i35Ut']")
        name_list = []
        for element in holding_name_elements:
            if element.text != "":
                name = element.text
                try:
                    if len(self.cbonds_etf_symbols) > 1:
                        name = re.split(r'[^a-zA-Z]+', name)[0].lower()
                    name_list.append(name)
                except:
                    print(f"Invalid name {name} found in holdings table")
                    continue

        return name_list

    @staticmethod
    def _get_perc_list(driver) -> list[float]:
        holding_perc_elements = driver.find_elements(By.XPATH, "//span[@class='Nobr_Nobr__f_hb7']")
        perc_list: list[float] = []
        for element in holding_perc_elements:
            text = element.text
            if text != "" and '%' in text:
                new_text = text.replace('%', '')
                if '<' in new_text:
                    new_text = '0.001'
                try:
                    float_value = float(new_text)
                    perc_list.append(float_value)
                except ValueError:
                    continue
        perc_list.pop()  # remove the last element as it is not a holding percentage but showing annual yield
        return perc_list

    '''
    :returns {ETF_NAME -> [...shares: {{percentage_of_etf: 0.0, name: "Apple Inc."}}]}
    '''

    def _get_etf_from_investengine(self, etf_symbol) -> ETF:
        driver = self._init_browser(etf_symbol, Platform.INVESTENGINE)
        etf_title = driver.find_element(By.XPATH,
                                        "//h1[@class='Text_Text_lineHeightDesktop_28__QNiM5 Text_Text_lineHeightMobile_28__26FYk Text_Text_sizeDesktop_24__gS4z_ Text_Text_sizeMobile_24__MAm_D Text_Text_weightDesktop_600__8pjBO Text_Text_weightMobile_600__CZXCB']").text
        name_list: list[str] = self._get_name_list(driver)
        perc_list: list[float] = self._get_perc_list(driver)

        share_list: list[Share] = []
        for i in range(len(name_list)):
            share_list.append(Share(name_list[i], etf_title, perc_list[i]))

        etf = ETF(etf_title, share_list)

        driver.quit()

        return etf

    @staticmethod
    def _click_show_more(driver):
        driver.find_element(By.XPATH, "//a[@class='cookie_panel_success']").click()
        elements = driver.find_elements(By.XPATH, "//a[@class='show_hide_block']")
        for element in elements:
            if 'Show more' in element.text:
                element.click()

    def _get_holdings_table(self, driver) -> pd.DataFrame:
        self._click_show_more(driver)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return pd.read_html(soup.prettify())[2]

    def _get_etf_from_cbonds(self, etf_symbol) -> ETF:
        driver = self._init_browser(etf_symbol, Platform.CBONDS)
        etf_title = driver.find_element(By.XPATH, "//h1[@class='main-ttl']").text
        holdings_table = self._get_holdings_table(driver)

        share_list: list[Share] = []
        for row in holdings_table.itertuples():
            row_perc = row.Value
            row_name: str = row.Paper
            try:
                row_name = re.split(r'[^a-zA-Z]+', row_name)[0].lower()
            except:
                print(f"Invalid name {row_name} found in {etf_symbol} holdings table, at index: {row.Index}")
                continue

            if '%' in row_perc:
                perc = float(row_perc.replace('%', ''))
                share_list.append(Share(row_name, etf_title, perc))
            else:
                print(f"Invalid percentage {row_perc} found in {etf_symbol} holdings table, at index: {row.Index}")

        driver.quit()
        return ETF(etf_title, share_list)

    @staticmethod
    def _get_unique_tuple_combinations(elements: list[str]) -> list[tuple[str, str]]:
        """
        Precondition: `elements` does not contain duplicates.
        Postcondition: Returns unique combinations of length 2 from `elements`.

        >>> _get_unique_tuple_combinations(["apple", "orange", "banana"])
        [("apple", "orange"), ("apple", "banana"), ("orange", "banana")]
        """
        return list(itertools.combinations(elements, 2))

    @staticmethod
    def _convert_comparison_to_dataframe(platform: Platform, comparison: Comparison, etf1_symbol: str,
                                         etf2_symbol: str) -> pd.DataFrame:
        common_share_dict_list = [
            {"Common Share": common_share.name, "% of ETF": np.round(common_share.percentage_of_etf, 2)} for
            common_share in
            comparison.common_shares]
        common_share_df = pd.DataFrame(common_share_dict_list)
        summary_df = pd.DataFrame([{"Common Shares": len(comparison.common_shares),
                                    etf1_symbol + " % Similar": np.round(
                                        comparison.etf1_perc, 2),
                                    etf2_symbol + " % Similar": np.round(
                                        comparison.etf2_perc, 2)}])
        return pd.concat([common_share_df, summary_df], axis=1)

    @staticmethod
    def _write_to_file(i: int, df: pd.DataFrame, writer, title: str) -> int:
        df.to_excel(writer, sheet_name=title, index=False)
        return i + 1

    def _platform_generate_report(self, platform: Platform):
        etfs: dict[str, list[Share]] = {}
        for symbol in self.investengine_etf_symbols:
            etf: ETF = self._get_etf_from_investengine(symbol)
            etfs[etf.name] = etf.shares
        for symbol in self.cbonds_etf_symbols:
            etf: ETF = self._get_etf_from_cbonds(symbol)
            etfs[etf.name] = etf.shares

        if len(etfs) > 1:
            unique_combinations = self._get_unique_tuple_combinations(list(etfs.keys()))
            i = 0
            with pd.ExcelWriter(self.FILE_PATH) as writer:
                for combo in unique_combinations:
                    comparison: Comparison = Comparison(etfs[combo[0]], etfs[combo[1]])
                    # write to file
                    title = ('Comparison between ' + combo[0] + ' and ' + combo[1])
                    i = self._write_to_file(i, self._convert_comparison_to_dataframe(platform, comparison, combo[0],
                                                                                     combo[1]), writer, title)
            print(f"Comparison file written to {self.FILE_PATH}")
        else:
            print("Only one ETF provided, no comparison to be made")

    def generate_report(self):
        self._platform_generate_report(self.platform)


def main():
    downloader = ETFDiversificationCalculator()
    downloader.generate_report()


if __name__ == "__main__":
    main()
