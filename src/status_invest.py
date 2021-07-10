import requests
import logging
import bs4
import pandas
import numpy as np


def get_ibrx_info(url: str, logger: logging.Logger) -> set:
    """Returns set with IRX100 index

    :param url: status invest url
    :type url: str 
    :param logger: Logger object
    :type logger: logging.Logger
    :return: set with IRX100 index
    :rtype: set
    """
    logger.info(f'Processing url: {url}')
    
    bs = bs4.BeautifulSoup(requests.get(url, verify=True).content, "html.parser")
    tickers_ibrx100 = set([x.text for x in list(bs.find_all("span", {"class": "ticker"}))])
    
    logger.info(f'Returned {len(tickers_ibrx100)} tickers')
    
    return tickers_ibrx100


def get_ticker_roic_info(url: str) -> dict:
    """Returns ibrx100 index informations

    :param url: status invest url
    :type url: str 
    :return: Dictionary with ibrx100 index informations
    :rtype: dict
    """
    tickers_info = requests.get(url).content

    df: pandas.DataFrame = pandas.read_json(tickers_info)
    df = df.sort_values('roic', ascending=False)
    
    df['roic'] = df['roic'].replace(np.NaN, 0)
    df['roic_index'] = [x for x, y in enumerate(df['roic'].iteritems())]
    
    df = df[['ticker', 'roic_index', 'roic']]
    df.set_index(['ticker'], inplace=True)
    # df.to_excel(
    #     excel_writer=f'{XLSX_PATH}roic_info_{datetime.datetime.now().strftime("%Y%m%d")}.xlsx',
    #     sheet_name='stocks', index=True, engine='openpyxl', freeze_panes=(1, 0),
    # )
    
    return df.to_dict('index')
