
class PreScrapedOkidokiProduct:
    id: str #Okidoki Product ID
    name: str
    href: str
    def __init__(self, id, name, href):
        self.id = id
        self.name = name
        self.href = href