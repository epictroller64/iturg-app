from database import select
from factory import LoggerFactory
import re

class Result:
    device: str
    chip: str
    ram: str
    screen_size: str
    generation: str
    storage: str
    color: str
    status: str
    year: str
    watch_mm: str

    def __init__(self):
        self.device = ""
        self.chip = ""
        self.ram = ""
        self.screen_size = ""
        self.generation = ""
        self.storage = ""
        self.color = ""
        self.status = ""
        self.year = ""
        self.watch_mm = ""

class Classifier:
    """Trying different way to classify main features of the product"""

    def __init__(self):
        self.logger = LoggerFactory.get_logger("Classifier")

    async def test(self):
        rows = await select("SELECT * FROM level1_groups")
        grouped_by_product = {}
        
        for row in rows:
            product_id = row['product_table_id']
            group_value = row['group_value']
            
            if product_id not in grouped_by_product:
                grouped_by_product[product_id] = []
            
            grouped_by_product[product_id].append(group_value)
        
        groups = [
            values
            for product_id, values in grouped_by_product.items()
        ]
        
        for group in groups:
            result = self.classify_features(group)
            print("\n" + "="*50)
            print(f"Device:      {result.device}")
            print(f"Chip:        {result.chip}")
            print(f"RAM:         {result.ram}")
            print(f"Screen:      {result.screen_size}")
            print(f"Generation:  {result.generation}")
            print(f"Storage:     {result.storage}")
            print(f"Color:       {result.color}")
            print(f"Status:      {result.status}")
            print(f"Year:        {result.year}")
            print(f"Watch Size:  {result.watch_mm}")
            print("="*50)

    def classify_features(self, features: list[str]) -> Result:
        result = Result()
        result = self.classify_device(features, result)
        result = self.classify_chip(features, result)
        result = self.classify_screen_size(features, result)
        result = self.classify_generation(features, result)
        result = self.classify_storage(features, result)
        result = self.classify_ram(features, result)
        result = self.classify_color(features, result)
        result = self.classify_status(features, result)
        result = self.classify_year(features, result)
        result = self.classify_watch_mm(features, result)
        return result
    
    def classify_watch_mm(self, features: list[str], result: Result) -> Result:
        if result.device.startswith("watch"):
            for feature in features:
                mm_pattern = r"(\d+)\s*mm"
                match = re.search(mm_pattern, feature.lower())
                if match:
                    result.watch_mm = f"{match.group(1)}mm"
                    features.remove(feature)
                    break
        return result

    def classify_status(self, features: list[str], result: Result) -> Result:
        for feature in features:
            if "new" in feature.lower():
                result.status = "uus"
                features.remove(feature)
                break
            elif "uus" in feature.lower():
                result.status = "uus"
                features.remove(feature)
                break
            elif "used" in feature.lower():
                result.status = "kasutatud"
                features.remove(feature)
                break
        return result

    def classify_storage(self, features: list[str], result: Result) -> Result:
        for feature in features:
            storage_pattern = r"(\d+)\s*(?:gb|tb)"
            match = re.search(storage_pattern, feature.lower())
            if match:
                storage_value = int(match.group(1))
                if storage_value >= 64:
                    if "tb" in feature.lower():
                        result.storage = f"{storage_value}TB"
                    else:
                        result.storage = f"{storage_value}GB"
                    features.remove(feature)
                    break
            elif "storage" in feature.lower():
                result.storage = feature
                features.remove(feature)
                break
        return result


    def classify_chip(self, features: list[str], result: Result) -> Result:
        for feature in features:
            m_chip_pattern = r"(m[1-4](?:\s*(?:pro|pro\s*max)?))(?:\s|$)"
            match = re.search(m_chip_pattern, feature.lower())
            if match:
                result.chip = match.group(1).replace(" ", "")  
                features.remove(feature)
                break

            intel_pattern = r"((?:i[3579])(?:-\d{4,5}[a-z]*)?)"
            match = re.search(intel_pattern, feature.lower())
            if match:
                result.chip = match.group(1)
                features.remove(feature)
                break
        return result
    
    def classify_screen_size(self, features: list[str], result: Result) -> Result:
        for feature in features:
            screen_size_pattern = r"(\d+(\.\d+)?)\s*(?:inch|tolli|tolline|\")"
            match = re.search(screen_size_pattern, feature.lower())
            if match:
                screen_size = match.group(1)  # Extract just the number
                result.screen_size = f"{screen_size}"  # Format with inch symbol
                features.remove(feature)
                break
        return result
    
    def classify_generation(self, features: list[str], result: Result) -> Result:
        for feature in features:
            if result.device == "watch":
                series_pattern = r"series\s*(\d+)"
                match = re.search(series_pattern, feature.lower())
                if match:
                    generation_value = match.group(1)
                    result.generation = generation_value
                    features.remove(feature)
                    break
            else:
                ordinal_pattern = r"(\d+)(?:st|nd|rd|th)\s*(?:generation|generatsioon)"
                match = re.search(ordinal_pattern, feature.lower())
                if match:
                    generation_value = match.group(1)
                    result.generation = generation_value
                    features.remove(feature)
                    break

                generation_pattern = r"(?:generation|generatsioon)\s*(\d+)"
                match = re.search(generation_pattern, feature.lower())
                if match:
                    generation_value = match.group(1)
                    result.generation = generation_value
                    features.remove(feature)
                    break
        return result
    

    def classify_ram(self, features: list[str], result: Result) -> Result:
        for feature in features:
            ram_pattern = r"(\d+)\s*(?:gb|ram)"
            match = re.search(ram_pattern, feature.lower())
            if match:
                ram_value = int(match.group(1))
                if ram_value < 64:
                    result.ram = f"{ram_value}GB RAM"  
                    features.remove(feature)
                break
        return result
    

    def classify_device(self, features: list[str], result: Result) -> Result:
        result = self.is_ipad(features, result)
        result = self.is_macbook(features, result)
        result = self.is_iphone(features, result)
        result = self.is_watch(features, result)
        result = self.is_apple_tv(features, result)
        result = self.is_airpods(features, result)
        result = self.is_imac(features, result)
        return result
    
    def is_airpods(self, features: list[str], result: Result) -> Result:
        for feature in features:
            if "airpods" in feature.lower():
                result.device = "Airpods"
                if "airpods 2" in feature.lower():
                    result.device = "Airpods 2"
                elif "airpods 3" in feature.lower():
                    result.device = "Airpods 3"
                elif "airpods pro" in feature.lower():
                    result.device = "Airpods Pro"
                features.remove(feature)
                break
        return result
    
    def is_apple_tv(self, features: list[str], result: Result) -> Result:
        for feature in features:
            if "apple tv" in feature.lower():
                result.device = "Apple TV"
                features.remove(feature)
                break
        return result

    def is_watch(self, features: list[str], result: Result) -> Result:
        for feature in features:
            if "watch" in feature.lower():
                result.device = "Watch"
                if "se" in feature.lower():
                    result.device = f"{result.device} SE"
                elif "se2" in feature.lower():
                    result.device = f"{result.device} SE2"
                features.remove(feature)
                break
        return result
    
    def is_imac(self, features: list[str], result: Result) -> Result:
        for feature in features:
            if "imac" in feature.lower():
                result.device = "iMac"
                features.remove(feature)
                break
        return result

    def is_ipad(self, features: list[str], result: Result) -> Result:
        for feature in features:
            if "ipad" in feature.lower():
                result.device = "iPad"
                if "pro" in feature.lower():
                    result.device = "iPad Pro"
                    ipad_pattern = r"ipad\s+pro\s*(\d+)"
                    match = re.search(ipad_pattern, feature.lower())
                    if match:
                        result.device = f"iPad Pro {match.group(1)}"
                elif "mini" in feature.lower():
                    result.device = "iPad Mini"
                    ipad_pattern = r"ipad\s+mini\s*(\d+)"
                    match = re.search(ipad_pattern, feature.lower())
                    if match:
                        result.device = f"ipad mini {match.group(1)}"
                elif "air" in feature.lower():
                    result.device = "iPad Air"
                    ipad_pattern = r"ipad\s+air\s*(\d+)"
                    match = re.search(ipad_pattern, feature.lower())
                    if match:
                        result.device = f"iPad Air {match.group(1)}"
                features.remove(feature)
                break
        return result
    
    def classify_color(self, features: list[str], result: Result) -> Result:
        matches = {
            "midnight": "Midnight",
            "black": "Must",
            "purple": "Purple",
            "space gray": "Space-grey",
            "must": "Must", 
            "red": "Punane",
            "gold": "Kuldne",
            "punane": "Punane",
            "white": "Valge",
            "valge": "Valge",
            "space grey": "Space-grey",
            "green": "Roheline",
            "desert titanium": "Desert-titanium",
            "black titanium": "Must-titaanium",
            "natural titanium": "Naturaalne-titaanium",
            "pink": "Pink",
            "blue": "Sinine",
            "sinine": "Sinine",
            "starlight": "Starlight",
        }
        for feature in features:
            for match in matches:
                if match in feature.lower():
                    result.color = match
                    features.remove(feature)
                    break
        return result

    def is_iphone(self, features: list[str], result: Result) -> Result:
        for feature in features:
            if "iphone" in feature.lower():
                result.device = "iPhone"
                # Use regex to extract iPhone model number
                iphone_pattern = r"(?:iphone\s*)?(\d{1,2})"
                match = re.search(iphone_pattern, feature.lower())
                if match:
                    model_number = match.group(1)
                    result.device = f"iPhone {model_number}"
                    if "pro" in feature.lower():
                        result.device = f"{result.device} Pro"
                    if "max" in feature.lower():
                        result.device = f"{result.device} Max"
                    if "plus" in feature.lower():
                        result.device = f"{result.device} Plus"
                features.remove(feature)
                break
        return result

    def is_macbook(self, features: list[str], result: Result) -> Result:
        patterns = [
            r"macbook(?:\s+(?:air|pro))?",  # Matches macbook, macbook air, macbook pro
            r"mb(?:\s+(?:air|pro))?",       # Matches mb, mb air, mb pro
            r"mac\s*book"                    # Matches mac book, macbook with optional space
        ]
        for pattern in patterns:
            for feature in features:
                if re.search(pattern, feature, re.IGNORECASE):
                    result.device = "MacBook"
                    if "pro" in feature.lower():
                        result.device = "MacBook Pro"
                    elif "air" in feature.lower():
                        result.device = "MacBook Air"
                    features.remove(feature)
                    break
        return result

    def classify_year(self, features: list[str], result: Result) -> Result:
        for feature in features:
            # Match both standalone years and years followed by "model" or "mudel"
            year_pattern = r"(\d{4})(?:\s*(?:model|mudel))?"
            match = re.search(year_pattern, feature.lower())
            if match:
                year = int(match.group(1))
                if year > 2016 and year < 2025:
                    result.year = str(year)
                    features.remove(feature)
                    break
        return result