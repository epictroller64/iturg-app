
class PreScrapedSoovProduct:
    id: str
    name: str
    href: str
    price: float
    def __init__(self, id, name, href, price):
        self.id = id
        self.name = name
        self.href = href
        self.price = price

