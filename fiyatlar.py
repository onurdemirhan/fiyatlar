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
    product_prices = {}
    if url.status_code == 429:
        return product_prices
    soup = BeautifulSoup(data, "html.parser")
    product_elements = soup.find(class_="cACjAF")
    product_elements = product_elements.find_all(id="cimri-product")
    for element in product_elements:
        try:
            product_title = element.contents[0].find_all(
                class_="link-detail")[0].attrs["title"]
            if element.contents[0].find_all(class_="top-offers")[0].contents[
                    0].next_element.nextSibling is None:  #if price is null
                continue
            product_price = float(
                element.contents[0].find_all(class_="top-offers")[0].
                contents[0].next_element.nextSibling.split(" TL")[0].replace(
                    ".", "").replace(",", "."))
            product_prices[webpage["params"]["q"] + " @ " +
                           product_title] = (product_price)
        except (IndexError, AttributeError) as error:
            print(error, webpage["url"].split(".")[1])  # handle error
    return dict(sorted(product_prices.items(), key=lambda x: x[1])[:2])


def akakce(webpage):
    with requests.get(webpage["url"],
                      params=webpage["params"],
                      headers=headers) as url:
        data = url.content
    product_prices = {}
    if url.status_code == 429:
        return product_prices
    soup = BeautifulSoup(data, "html.parser")
    product_elements = soup.find(id="APL").find_all("li")
    product_prices = {}
    for element in product_elements:
        try:
            product_title = element.find_all(class_="pn_v8")[0].text
            product_price = float(
                element.find_all(
                    class_="pt_v9")[0].text.split("TL")[0].strip().replace(
                        ".", "").replace(",", "."))
            product_prices[webpage["params"]["q"] + " @ " +
                           product_title] = product_price
        except (IndexError, AttributeError) as error:
            print(error, webpage["url"].split(".")[1])  # handle error
    return dict(sorted(product_prices.items(), key=lambda x: x[1])[:2])


def epey(webpage):
    webpage["params"]["ara"] = webpage["params"]["q"]
    webpage["params"].pop("q")
    with requests.get(webpage["url"],
                      params=webpage["params"],
                      headers=headers) as url:
        data = url.content
    product_prices = {}
    if url.status_code == 429:
        return product_prices
    soup = BeautifulSoup(data, "html.parser")
    product_elements = soup.find_all(class_="listele table")[0].find_all("ul")
    product_prices = {}
    for element in product_elements:
        try:
            if element.find(
                    class_="fiyat cell").find("a") is None or element.find(
                        class_="fiyat cell") is None:  #if product is NA
                continue
            product_title = element.find(class_="urunadi").text
            product_price = float(
                element.find(class_="fiyat cell").find("a").next_element.split(
                    "TL")[0].strip().replace(".", "").replace(",", "."))
            product_prices[webpage["params"]["ara"] + " @ " +
                           product_title] = product_price
            sorted(product_prices.items(), )
        except (IndexError, AttributeError) as error:
            print(error, webpage["url"].split(".")[1])  # handle error

    return dict(sorted(product_prices.items(), key=lambda x: x[1])[:2])


queries = [
    "Radeon RX 7900 XTX", "Radeon RX 7900 XT", "Radeon RX 6950 XT",
    "Radeon RX 6900 XT", "Radeon RX 6800 XT", "Radeon RX 6800",
    "Radeon RX 6750 XT", "Radeon RX 6700 XT", "Radeon RX 6700",
    "Radeon RX 6650 XT", "Radeon RX 6600 XT", "Radeon RX 6600",
    "Radeon RX 6500 XT", "GeForce RTX 3090 Ti", "GeForce RTX 3090",
    "GeForce RTX 3080 Ti", "GeForce RTX 3080", "GeForce RTX 3070 Ti",
    "GeForce RTX 3070", "GeForce RTX 3060", "GeForce RTX 3050"
]

WEBSITES = {
    "cimri": {
        "url": "https://www.cimri.com/ekran-kartlari",
        "params": {
            "q": ""
        },
    },
    "akakce": {
        "url": "https://www.akakce.com/arama/",
        "params": {
            "q": "",
            "c": "1053"
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
    for query in queries:
        for website in WEBSITES:
            func = globals()[website]
            WEBSITES[website]['params']['q'] = query
            if website not in prices:
                prices[website] = {}
            price = func(WEBSITES[website])
            if price == {}:
                prices[website].update({f"{query} @ " : ""})
            else:
                prices[website].update(price)
    for website in prices:
        for item, price in prices[website].items():
            print(f"{item}: {price} @ {website}")
    return prices
    


if __name__ == '__main__':
    main()