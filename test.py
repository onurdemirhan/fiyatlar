WEBSITES = {
    "CIMRI": "https://www.cimri.com/arama?sort=price%2Casc&q=radeon+6750+xt",
    "AKAKCE": "https://www.akakce.com/arama/?q=6750+XT&s=2",
    "EPEY":
    "https://www.epey.com/ekran-karti/grafik-islemcisi/radeon-rx-6750-xt",
}


def main():
    websites = {name: fetch_prices(url) for name, url in WEBSITES.items()}
    sorted_prices = merge_prices(websites)

    print_prices("CIMRI", websites["CIMRI"])
    print_prices("AKAKCE", websites["AKAKCE"])
    print_prices("EPEY", websites["EPEY"])
    print_prices("HEPSI", sorted_prices)


def fetch_prices(url):
    # TODO: Implement the logic to fetch prices from a website
    pass


def merge_prices(websites):
    sorted_prices = {}
    for prices in websites.values():
        sorted_prices.update(prices)
    return dict(sorted(sorted_prices.items(), key=lambda x: x[1]))


def print_prices(name, prices):
    print(f"\n***{name}***")
    for title, price in prices.items():
        print(f"{title} @ {price}")
