from bs4 import BeautifulSoup
import requests


def cimri(webpage):
    headers = {
        'User-Agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    with requests.get(webpage, headers=headers) as url:
        data = url.content
    soup = BeautifulSoup(data, "html.parser")
    product_elements = soup.find_all(id="cimri-product")
    product_prices = {}
    for element in product_elements:
        product_title = element.contents[0].find_all(
            class_="link-detail")[0].attrs["title"]
        product_price = element.contents[0].find_all(
            class_="top-offers")[0].contents[0].next_element.nextSibling
        product_prices[product_title] = product_price
    return product_prices


def akakce(webpage):
    headers = {
        'User-Agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    with requests.get(webpage, headers=headers) as url:
        data = url.content
    soup = BeautifulSoup(data, "html.parser")
    product_elements = soup.find_all("li")
    product_prices = {}
    for element in product_elements:
        try:
            product_title = element.find_all(class_="pn_v8")[0].text
            product_price = element.find_all(
                class_="pt_v9")[0].text.split("TL")[0].strip()
            product_prices[product_title] = product_price
        except IndexError:
            pass  # handle error
    return product_prices

def epey(webpage):
    headers = {
        'User-Agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    with requests.get(webpage, headers=headers) as url:
        data = url.content
    soup = BeautifulSoup(data, "html.parser")
    product_elements = soup.find_all("li")
    product_prices = {}
    for element in product_elements:
        try:
            product_title = element.find_all(class_="pn_v8")[0].text
            product_price = element.find_all(
                class_="pt_v9")[0].text.split("TL")[0].strip()
            product_prices[product_title] = product_price
        except IndexError:
            pass  # handle error
    return product_prices




def main():
    cimri_webpage = "https://www.cimri.com/arama?sort=price%2Casc&q=radeon+6800+xt"
    akakce_webpage = "https://www.akakce.com/arama/?q=6750+XT&s=2"
    cimri_prices = cimri(cimri_webpage)
    akakce_prices = akakce(akakce_webpage)
    print("\n cimri BASLIYOR")
    for title, price in cimri_prices.items():
        print(title, "@", price)
    print("\n akakce BASLIYOR ")
    for title, price in akakce_prices.items():
        print(title, "@", price)


if __name__ == '__main__':
    main()
