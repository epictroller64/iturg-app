from database import execute, execute_batch
from factory import LoggerFactory
from classifier import Classifier

class GroupPipeline:

    def __init__(self):
        self.logger = LoggerFactory.get_logger("GroupPipeline")
        self.classifier = Classifier()
        self.ignore_groups = ["Ümbrised", "WiFi", "Bluetooth", "Kõik", "kõrvaklapid", "kõrvaklappid", "Apple", "wi-fi", "karp", "laadija", "sulearvuti", "cellular connectivity", ""]
        self.delete_words = [" case size", " display", ]
        self.splittable_groups = ["macbook air", "macbook pro", ]

    async def process_groups(self, features: list[str], product_table_id: int):

        result = self.classifier.classify_features(features)

        result_tuple = (
            product_table_id,
            result.device,
            result.chip,
            result.ram,
            result.screen_size,
            result.generation,
            result.storage,
            result.color,
            result.status,
            result.year,
            result.watch_mm
        )
        
        # Lets insert them into the database
        group1_values = [(feature, product_table_id) for feature in features]
        await execute_batch('INSERT OR IGNORE INTO level1_groups (group_value, product_table_id) VALUES (?, ?)', group1_values)

        # Now lets insert the level 2 groups
        await execute('INSERT OR IGNORE INTO level2_groups (product_table_id, device, chip, ram, screen_size, generation, storage, color, status, year, watch_mm) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', result_tuple)

        self.logger.info(f"Processed groups for {product_table_id}")

