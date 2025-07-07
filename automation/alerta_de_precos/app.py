"""Alerta de Preços - Automatização de Consulta de Preços de Produtos em Sites de E-commerce"""

from lxml import html
from lxml.html import fromstring
import requests
from time import sleep
import time
import schedule
import argparse
import locale
import random
import sys
import csv
from pathlib import Path
import datetime
import os
import configparser
from bs4 import BeautifulSoup as bs
from fp.fp import FreeProxy

LOG_FILE_PATH = os.path.dirname(os.path.realpath(__file__))

proxy_list = []

logfile = False
# Tempo de espera entre as execuções do script (em minutos) - default 15 minutos
timeframe = 15


def tslog(msg, logtofile=False, logfilesufix="_log.txt", path=""):
    """Função para registrar logs de execução do script"""

    global LOG_FILE_PATH
    global logfile

    if LOG_FILE_PATH:
        path = LOG_FILE_PATH

    dateTimeObj = datetime.datetime.now()

    timestampStr = dateTimeObj.strftime("%Y-%m-%d")

    if path:
        timestampStr = timestampStr

    if logfile or logtofile:
        f = open(os.path.join(path, timestampStr + logfilesufix), "a")
        f.write(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S%z ") + ";" + msg + "\n"
        )
        f.close()

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S%z ") + " - " + msg)


def check_if_proxy_is_working(proxies: str, timeout: int = 10) -> (bool | None):
    """Função para verificar se um proxy está funcionando corretamente"""
    try:
        with requests.get(
            "https://www.amazon.com.br", proxies=proxies, timeout=timeout, stream=True
        ) as r:
            if r.raw.connection.sock:
                if (
                    r.raw.connection.sock.getpeername()[0]
                    == proxies["https"].split(":")[1][2:]
                ):
                    tslog("Proxy %s OK!" % proxies["https"])
                    return True
            else:
                tslog(
                    "Proxy %s não OK - Peer: %s"
                    % (proxies["https"], r.raw.connection.sock.getpeername()[0])
                )
                return False
    except (
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ReadTimeout,
        requests.exceptions.ProxyError,
        requests.exceptions.SSLError,
    ) as e:
        tslog("Proxy %s não OK - Error: %s" % (proxies["https"], e))


def get_proxies():
    """Função para obter uma lista de proxies válidos"""

    url = "https://free-proxy-list.net/"
    tslog("Loading proxy list from: %s" % url)

    # url = 'https://www.sslproxies.org'
    country_id = ["BR", "US", "CA", "DE", "ID", "JP", "IN", "RU", "MX", "GB", "AR"]
    # country_id = False
    anonym = False
    ssl = True

    try:
        response = requests.get(url)
        parser = fromstring(response.content)
    except requests.exceptions.RequestException as e:
        tslog("Error getting proxies - connection error # %s " % e)
        return None

    proxies = []

    tr_elements = parser.xpath('//*[@id="proxylisttable"]//tr')
    # tr_elements = parser.xpath('//tbody/tr')[:20]

    for i in tr_elements:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join(
                [i.xpath(".//td[1]/text()")[0], i.xpath(".//td[2]/text()")[0]]
            )
            proxies.append(proxy)

    for i in range(1, 101):
        if (
            (tr_elements[i][2].text_content() in country_id if country_id else True)
            and ((tr_elements[i][4].text_content()) == "anonymous" if anonym else True)
            and ((tr_elements[i][6].text_content()) == "yes" if ssl else True)
        ):
            proxy = {
                "https": "http://"
                + tr_elements[i][0].text_content()
                + ":"
                + tr_elements[i][1].text_content(),
            }

            if check_if_proxy_is_working(proxy):
                proxies.append(
                    tr_elements[i][0].text_content()
                    + ":"
                    + tr_elements[i][1].text_content()
                )

    # check the 5th column for `anonymous` if needed
    proxies = [
        f"{tr_elements[i][0].text_content()}:{tr_elements[i][1].text_content()}"
        for i in range(1, 101)
        if tr_elements[i][2].text_content() in country_id
        and ((tr_elements[i][4].text_content()) == "anonymous" if anonym else True)
        and ((tr_elements[i][6].text_content()) == "yes" if ssl else True)
    ]

    return proxies


def get_user_agent() -> str:
    """Função para obter um user agent aleatório"""

    user_agent_list = [
        # Chrome
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        # Firefox
        "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
    ]
    user_agent = random.choice(user_agent_list)
    return user_agent


def connect(url: str, proxy: str, headers: str) -> None:
    """Função para conectar a um site e obter o conteúdo da página"""

    r1 = None

    try:
        if proxy:
            tslog("Using proxy: " + proxy)
            r1 = requests.get(
                url,
                headers=headers,
                proxies={"http": proxy, "https": proxy},
                timeout=20,
            )

        else:
            tslog("No proxie connection...")
            r1 = requests.get(url, headers=headers)

    except requests.exceptions.RequestException as e:
        tslog("Main: Erro de conexão... Tentando novamente %s" % e)
        return None
    except requests.exceptions.ConnectTimeout as et:
        tslog("Main: Erro de conexão, Timeout ... Tentando novamente %s" % et)
        return None

    # check for error http
    if r1.status_code != 200:
        tslog("Error while browsing in, code: %d" % r1.status_code)
        r1 = None

    return r1


def mk_float(s: str) -> float:
    """Função para converter uma string em float"""
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    s = s.replace("R$", "")
    s = locale.atof(s)
    return float(s) if s else 0


def amazoncheck(url: str) -> None:
    """Função para verificar a disponibilidade e preço de um produto no site da Amazon"""

    availabiliy = ""
    title = ""
    proxy = ""
    global proxy_list
    # adding headers to pretend being a regular browser

    tslog("Open url: " + url)

    user_agent = get_user_agent()

    headers = {
        "User-Agent": user_agent,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "pt-BR,en-GB,en-US;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }

    # proxy_list = FreeProxy(country_id=['US', 'BR']).get()

    page = False

    i = 0

    while not page:
        if proxy_list:
            proxy = random.choice(proxy_list)

            page = connect(url, proxy, headers)
        i += 1
        sleep(3)

        if i > 5:
            break

    if not page:
        tslog("Connection error... Proxy: %s" % proxy)
        return "", "", ""

    sleep(1)

    soup = bs(page.content, "html.parser")

    try:
        if soup.select_one('input[id="captchacharacters"]'):
            tslog("Página de captcha, reconectando...")
            return "", "", ""

        title = soup.select_one('h1[id="title"]').text
        title = "".join(title).strip() if title else ""
        tslog("Título: %s" % title)

        availabiliy = soup.select_one('div[id="availability"]').text
        availabiliy = "".join(availabiliy).strip() if availabiliy else ""

    except AttributeError as err:
        tslog("Erro na leitura da página: %s" % err)
        price = 0

    try:
        price = soup.select_one('div[id="priceInsideBuyBox_feature_div"]').text

        price = "".join(price).strip() if price else 0
        if price == "" and "Em estoque" in availabiliy:
            # priceblock_ourprice
            price = soup.select_one('span[id="priceblock_ourprice"]').text
            price = "".join(price).strip() if price else 0

        price = mk_float(price.replace("R$", ""))
    except AttributeError as err1:
        price = 0

    return availabiliy, price, title


def readAsin(asin="B077PWK5BT", price=0.0):
    """Função para ler o código ASIN de um produto e verificar seu preço"""

    # Asin Id is the product Id which
    # needs to be provided by the user

    url = "https://www.amazon.com.br/dp/" + asin
    tslog("Processing: " + url)

    ans, price_real, title = amazoncheck(url)

    if not title:
        return

    arr = ["Only 1 left in stock.", "Only 2 left in stock.", "Em estoque."]
    if ans in arr:
        tslog("Produto %s - Preço: R$%s" % (title, price_real))
    else:
        tslog("Produto %s Indisponível" % title)
    # print(ans)

    if ans in arr and price == 0:
        subject = "[ALARME] Produto em estoque: %s" % title
        body = "[ALARME] Produto em estoque: %s \n Link para o site: %s" % (title, url)

        print(subject)
        print(body)

    if ans in arr and price > 0 and price_real < price:
        subject = "[ALARME] Preço menor para %s" % title
        body = "Preço menor para %s, preço: %s \n Link para o site: %s" % (
            title,
            price_real,
            url,
        )
        print(subject)
        print(body)


def job() -> None:
    """Função para iniciar o processo de rastreamento de preços"""

    global proxy_list

    CLI = argparse.ArgumentParser(add_help=False)

    CLI.add_argument("-f", "--file", help="Prices CSV File", default="products.csv")

    args = CLI.parse_args()

    # print(args)

    if args.file:
        csv_file = args.file

        my_file = Path(csv_file)
        if not my_file.is_file():
            tslog("DB file does NOT exists, no products to browse, correct it!", True)
            sys.exit()

        with open(csv_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            line_count = 0

            while not proxy_list:
                proxy_list = get_proxies()

                if proxy_list:
                    break
                else:
                    tslog("Trying to get valid proxy list")

            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    asin = row[0]
                    price = float(row[1])
                    line_count += 1

                    tslog("Tracking: %s - Price checking = %s" % (asin, price))
                    readAsin(asin, price)
        tslog("Fim do processo - aguardar timer")


if __name__ == "__main__":
    tslog("Initiating... Tracking every %s minutes" % timeframe, True)

    schedule.every(timeframe).minutes.do(job)
    runs = 0
    while True:
        n = schedule.idle_seconds()

        if runs > 0:
            # running all pending tasks/jobs
            schedule.run_pending()
        else:
            schedule.run_all()

        time.sleep(1)
        runs += 1
