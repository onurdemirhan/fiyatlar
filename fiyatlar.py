from bs4 import BeautifulSoup
import requests
import tweepy

headers = {
    'User-Agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
}


def cimri(webpage):
    with requests.get(webpage["url"],
                      params=webpage["params"],
                      headers=headers) as url:
        data = url.content
    soup = BeautifulSoup(data, "html.parser")
    product_elements = soup.find(class_="cACjAF")
    product_elements = product_elements.find_all(id="cimri-product")
    product_prices = {}
    for element in product_elements:
        try:
            # product = element.contents[0].find(class_="cACjAF")
            product_title = element.contents[0].find_all(
                class_="link-detail")[0].attrs["title"]
            product_price = float(
                element.contents[0].find_all(class_="top-offers")[0].
                contents[0].next_element.nextSibling.split(" TL")[0].replace(
                    ".", "").replace(",", "."))
            product_prices[webpage["params"]["q"] + "@ " +
                           product_title] = (product_price)
        except (IndexError, AttributeError) as error:
            print(error)  # handle error
    product_prices = dict(
        sorted(product_prices.items(), key=lambda x: x[1])[:2])
    return product_prices


def akakce(webpage):
    with requests.get(webpage["url"],
                      params=webpage["params"],
                      headers=headers) as url:
        data = url.content
    soup = BeautifulSoup(data, "html.parser")
    # product_elements = soup.find_all("li")
    product_elements = soup.find(id="APL").find_all("li")
    product_prices = {}
    for element in product_elements:
        try:
            product_title = element.find_all(class_="pn_v8")[0].text
            product_price = float(
                element.find_all(
                    class_="pt_v9")[0].text.split("TL")[0].strip().replace(
                        ".", "").replace(",", "."))
            product_prices[webpage["params"]["q"] + "@ " +
                           product_title] = product_price
        except (IndexError, AttributeError) as error:
            print(error)  # handle error
    product_prices = dict(
        sorted(product_prices.items(), key=lambda x: x[1])[:2])
    return product_prices


def epey(webpage):
    webpage["params"]["ara"] = webpage["params"]["q"]
    webpage["params"].pop("q")
    with requests.get(webpage["url"],
                      params=webpage["params"],
                      headers=headers) as url:
        data = url.content
    soup = BeautifulSoup(data, "html.parser")
    product_elements = soup.find_all(class_="listele table")[0].find_all("ul")
    product_prices = {}
    for element in product_elements:
        try:
            if element.find(class_="fiyat cell").find("a") is None:
                continue
            product_title = element.find(class_="urunadi").text
            product_price = float(
                element.find(class_="fiyat cell").find("a").next_element.split(
                    "TL")[0].strip().replace(".", "").replace(",", "."))
            product_prices[webpage["params"]["ara"] + "@ " +
                           product_title] = product_price
            sorted(product_prices.items(), )
            # product_price = ""
        except (IndexError, AttributeError) as error:
            print(error)  # handle error
    product_prices = dict(
        sorted(product_prices.items(), key=lambda x: x[1])[:2])
    return product_prices


queries = [
    "Radeon RX 7900 XTX", "Radeon RX 7900 XT", "Radeon RX 6950 XT",
    "Radeon RX 6900 XT", "Radeon RX 6800 XT", "Radeon RX 6800",
    "Radeon RX 6750 XT", "Radeon RX 6700 XT", "Radeon RX 6700",
    "Radeon RX 6650 XT", "Radeon RX 6600 XT", "Radeon RX 6600",
    "Radeon RX 6500 XT"
]

WEBSITES = {
    "cimri": {
        "url": "https://www.cimri.com/arama",
        "params": {
            "q": ""
        },
    },
    "akakce": {
        "url": "https://www.akakce.com/arama/",
        "params": {
            "q": ""
        },
    },
    "epey": {
        "url": "https://www.epey.com/ara/",
        "params": {
            "ara": ""
        }
    },
}


def main():
    prices = {}
    for website in WEBSITES:
        func = globals()[website]
        for query in queries:
            WEBSITES[website]['params']['q'] = query
            if website + "_prices" not in prices:
                prices[website + "_prices"] = {}
            prices[website + "_prices"].update(func(WEBSITES[website]))
    for website in prices:
        for item, price in prices[website].items():
            print(f"{item}: {price} @ {website}")


if __name__ == '__main__':
    main()
