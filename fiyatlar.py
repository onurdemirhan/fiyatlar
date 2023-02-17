from bs4 import BeautifulSoup
import requests
import tweepy

headers = {
    'User-Agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
}


def cimri(webpage):
    with requests.get(webpage["url"],
                      params=webpage.get("params"),
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
            product_prices[product_title] = (product_price)
        except (IndexError, AttributeError) as error:
            print(error)  # handle error
    product_prices = dict(
        sorted(product_prices.items(), key=lambda x: x[1])[:2])
    return product_prices


def akakce(webpage):
    with requests.get(webpage["url"],
                      params=webpage.get("params"),
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
            product_prices[product_title] = product_price
        except (IndexError, AttributeError) as error:
            print(error)  # handle error
    product_prices = dict(
        sorted(product_prices.items(), key=lambda x: x[1])[:2])
    return product_prices


def epey(webpage):
    with requests.get(webpage["url"],
                      params=webpage.get("params"),
                      headers=headers) as url:
        data = url.content
    soup = BeautifulSoup(data, "html.parser")
    product_elements = soup.find_all(class_="listele table")[0].find_all("ul")
    product_prices = {}
    for element in product_elements:
        try:
            product_title = element.find(class_="urunadi").text
            if element.find(class_="fiyat cell").find("a") is not None:
                product_price = float(
                    element.find(class_="fiyat cell").find(
                        "a").next_element.split("TL")[0].strip().replace(
                            ".", "").replace(",", "."))
            product_prices[product_title] = product_price
            sorted(product_prices.items(), )
        except (IndexError, AttributeError) as error:
            print(error)  # handle error
    product_prices = dict(
        sorted(product_prices.items(), key=lambda x: x[1])[:2])
    return product_prices


query = "Radeon RX 6750 XT"

WEBSITES = {
    "cimri": {
        "url": "https://www.cimri.com/arama",
        "params": {
            "sort": "price,asc",
            "q": query
        },
    },
    "akakce": {
        "url": "https://www.akakce.com/arama/",
        "params": {
            "q": query,
            "s": "2"
        },
    },
    "epey": {
        "url":
        "https://www.epey.com/ekran-karti/grafik-islemcisi/" +
        query.replace(" ", "-"),
        "params":
        ""
    },
}

# cimri_webpage = "https://www.cimri.com/arama?sort=price%2Casc&q=radeon+6750+xt"
# akakce_webpage = "https://www.akakce.com/arama/?q=6750+XT&s=2"
# epey_webpage = "https://www.epey.com/ekran-karti/grafik-islemcisi/radeon-rx-6750-xt"


def main():
    prices = {}
    for website in WEBSITES:
        func = globals()[website]
        prices[website + "_prices"] = func(WEBSITES[website])
    for website in prices:
        for item, price in prices[website].items():
            print(f"{item}: {price} @{website}")


if __name__ == '__main__':
    main()
