from typing import List
from database import execute_batch
from factory import LoggerFactory
import re
from database import select

class GroupPipeline:

    def __init__(self):
        self.logger = LoggerFactory.get_logger("GroupPipeline")
        self.ignore_groups = ["Ümbrised", "WiFi", "Bluetooth", "Kõik", "kõrvaklapid", "kõrvaklappid", "Apple", "wi-fi", "karp", "laadija", "sulearvuti", "cellular connectivity", ""]
        self.delete_words = [" case size", " display", ]
        self.splittable_groups = ["macbook air", "macbook pro", ]

    async def process_groups(self, features: list[str], product_table_id: int):
        # Filter out the ignore groups, manually assigned
        values = [value for value in features if value not in self.ignore_groups]
        values = [value for value in values if len(value) > 1]

        #Further optimize the values by grouping different but similar features

        
        # Lets insert them into the database
        values = [(feature, product_table_id) for feature in values]
        await execute_batch('INSERT OR IGNORE INTO level1_groups (group_value, product_table_id) VALUES (?, ?)', values)
        self.logger.info(f"Processed groups for {product_table_id}")

    def optimize_features(self, features: list[str]) -> list[str]:
        # Define mapping for common variations
        feature_mapping = {
            r"m4\b": "M4 Chip",
            r"m4 chip": "M4 Chip",
            r"m3\b": "M3 Chip",
            r"m3 chip": "M3 Chip",
            r"m2\b": "M2 Chip",
            r"m2 chip": "M2 Chip",
            r"m1\b": "M1 Chip",
            r"m1 chip": "M1 Chip",

            
            r"(\d+)gb ram": r"\1GB RAM",
            r"(\d+)gb": r"\1GB",
            r"(\d+) gb": r"\1GB",
            
            r"(\d+)tb": r"\1TB",
            r"(\d+) tb": r"\1TB",
            
            r"(\d+(\.\d+)?)\"": r"\1 tolli",
            r"(\d+(\.\d+)?)\s*inch": r"\1 tolli", 
            r"(\d+(\.\d+)?) tolli": r"\1 tolli",
            r"(\d+)\s*mm": r"\1mm", # spaces between number and mm

            r"wifi": "WiFi",
            r"bluetooth": "Bluetooth",
        }
        
        optimized_features = []
        
        for feature in features:
            feature = feature.strip().lower()
            # Apply each pattern replacement
            for pattern, replacement in feature_mapping.items():
                feature = re.sub(pattern, replacement, feature, flags=re.IGNORECASE)
            optimized_features.append(feature)
            
        optimized_features = list(dict.fromkeys(optimized_features))

        optimized_features = self.optimize_storage_values(optimized_features)
        optimized_features = self.optimize_cpu_values(optimized_features)
        return optimized_features


    def optimize_model_year_values(self, features: list[str]) -> list[str]:
        for index, feature in enumerate(features):
            lowercase_feature = feature.lower()
            if "model" in lowercase_feature:
                year_value = ''.join(filter(str.isdigit, lowercase_feature))
                if year_value < 2014:
                    continue
                features[index] = f"{year_value} Mudel"
        return features

    def optimize_cpu_values(self, features: list[str]) -> list[str]:
        for index, feature in enumerate(features):
            lowercase_feature = feature.lower()
            cpu_value = ''.join(filter(str.isdigit, lowercase_feature))
            if "cpu" in lowercase_feature:
                # Extract numeric value from CPU string
                features[index] = f"{cpu_value}C CPU"
            elif "gpu" in lowercase_feature:
                features[index] = f"{cpu_value}C GPU"
        return features

    def optimize_storage_values(self, features: list[str]) -> list[str]:
        for index, feature in enumerate(features):
            lowercase_feature = feature.lower()
            if "gb" in lowercase_feature:
                # Extract numeric value from GB string
                storage_value = int(''.join(filter(str.isdigit, lowercase_feature)))
                # Compare and categorize storage sizes
                if storage_value < 64:
                ## dealing with RAM values
                    features[index] = f"{storage_value}GB RAM"
                else:
                    features[index] = f"{storage_value}GB Ketas"
            elif "tb" in lowercase_feature:
                features[index] = f"{storage_value}TB Ketas"
        return features

    def optimize_features(self, features: list[str]) -> list[str]:
        pass


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

    def classify_features(self, features: list[str]) -> list[str]:
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
            m_chip_pattern = r"m[1-4](?:\s*(?:pro|pro\s*max))?"
            if re.search(m_chip_pattern, feature.lower()):
                result.chip = feature.lower()
                features.remove(feature)
                break

            intel_pattern = r"(?:intel\s*)?(?:core\s*)?i[3579](?:-\d{4,5}[a-z]*)?"
            if re.search(intel_pattern, feature.lower()):
                result.chip = feature.lower()
                features.remove(feature)
                break
        return result
    
    def classify_screen_size(self, features: list[str], result: Result) -> Result:
        for feature in features:
            screen_size_pattern = r"(\d+(\.\d+)?)\s*(?:inch|tolli|tolline|\")"
            match = re.search(screen_size_pattern, feature.lower())
            if match:
                screen_size = match.group(1)  # Extract just the number
                result.screen_size = f"{screen_size}\""  # Format with inch symbol
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
        return result
    
    def is_airpods(self, features: list[str], result: Result) -> Result:
        for feature in features:
            if "airpods" in feature.lower():
                result.device = "airpods"
                if "airpods 2" in feature.lower():
                    result.device = "airpods 2"
                elif "airpods 3" in feature.lower():
                    result.device = "airpods 3"
                elif "airpods pro" in feature.lower():
                    result.device = "airpods pro"
                features.remove(feature)
                break
        return result
    
    def is_apple_tv(self, features: list[str], result: Result) -> Result:
        for feature in features:
            if "apple tv" in feature.lower():
                result.device = "apple tv"
                features.remove(feature)
                break
        return result

    def is_watch(self, features: list[str], result: Result) -> Result:
        for feature in features:
            if "watch" in feature.lower():
                result.device = "watch"
                if "se" in feature.lower():
                    result.device = f"{result.device} se"
                elif "se2" in feature.lower():
                    result.device = f"{result.device} se2"
                features.remove(feature)
                break
        return result

    def is_ipad(self, features: list[str], result: Result) -> Result:
        for feature in features:
            if "ipad" in feature.lower():
                result.device = "ipad"
                if "pro" in feature.lower():
                    result.device = "ipad pro"
                    ipad_pattern = r"ipad\s+pro\s*(\d+)"
                    match = re.search(ipad_pattern, feature.lower())
                    if match:
                        result.device = f"ipad pro {match.group(1)}"
                elif "mini" in feature.lower():
                    result.device = "ipad mini"
                    ipad_pattern = r"ipad\s+mini\s*(\d+)"
                    match = re.search(ipad_pattern, feature.lower())
                    if match:
                        result.device = f"ipad mini {match.group(1)}"
                elif "air" in feature.lower():
                    result.device = "ipad air"
                    ipad_pattern = r"ipad\s+air\s*(\d+)"
                    match = re.search(ipad_pattern, feature.lower())
                    if match:
                        result.device = f"ipad air {match.group(1)}"
                features.remove(feature)
                break
        return result
    
    def classify_color(self, features: list[str], result: Result) -> Result:
        matches = {
            "midnight": "midnight",
            "black": "must",
            "must": "must", 
            "red": "punane",
            "punane": "punane",
            "white": "valge",
            "valge": "valge",
            "space grey": "space-grey",
            "green": "roheline",
            "desert titanium": "desert-titanium",
            "black titanium": "must-titaanium",
            "natural titanium": "naturaalne-titaanium",
            "pink": "pink",
            "starlight": "starlight",
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
                result.device = "iphone"
                # Use regex to extract iPhone model number
                iphone_pattern = r"(?:iphone\s*)?(\d{1,2})"
                match = re.search(iphone_pattern, feature.lower())
                if match:
                    model_number = match.group(1)
                    result.device = f"iphone {model_number}"
                    if "pro" in feature.lower():
                        result.device = f"{result.device} pro"
                    if "max" in feature.lower():
                        result.device = f"{result.device} max"
                    if "plus" in feature.lower():
                        result.device = f"{result.device} plus"
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
                    result.device = "macbook"
                    if "pro" in feature.lower():
                        result.device = "macbook pro"
                    elif "air" in feature.lower():
                        result.device = "macbook air"
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
                if year > 2016:
                    result.year = str(year)
                    features.remove(feature)
                    break
        return result
