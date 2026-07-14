ENTITY_TYPE_MAP = {
        "company": "Company",
        "organization": "Company",
        "organisation": "Company",

        "framework": "Framework",

        "technology": "Technology",

        "product": "Product",

        "tool": "Tool",

        "api": "API",

        "research paper": "Research Paper",

        "cloud service": "Cloud Service",

        "dataset": "Dataset",

        "benchmark": "Benchmark",

        "person": "Person"
    }

RELATIONSHIP_MAP = {

        "announced": "ANNOUNCES",

        "supports": "SUPPORTS",

        "supports_framework": "SUPPORTS",

        "integrates with": "INTEGRATES_WITH",

        "integrates_with": "INTEGRATES_WITH",

        "partners with": "PARTNERS_WITH",

        "collaborates_with": "PARTNERS_WITH",

        "available through": "AVAILABLE_THROUGH",

        "available_through": "AVAILABLE_THROUGH"
    }

EVENT_TYPE_MAP = {

        "product release": "PRODUCT_RELEASE",

        "product_launch": "PRODUCT_LAUNCH",

        "partnership": "PARTNERSHIP",

        "api update": "API_UPDATE",

        "model update": "MODEL_UPDATE"
    }

class Normalizer:
    def __init__(self, data):
        self.data = data

    def normalize(self):
        self.normalize_entities()
        self.normalize_relationships()
        self.normalize_events()
        self.remove_duplicate_entities()
        return self.data

    def normalize_entities(self):
        for entity in self.data["entities"]:

            entity["name"] = entity["name"].strip()

            entity_type = entity["type"].strip().lower()

            entity["type"] = ENTITY_TYPE_MAP.get(
                entity_type,
                "UNKNOWN"
            )


    def normalize_relationships(self):

        for rel in self.data["relationships"]:

            rel["entity_name1"] = rel["entity_name1"].strip()

            rel["entity_name2"] = rel["entity_name2"].strip()

            relation = rel["relationship_type"].strip().lower()

            rel["relationship_type"] = RELATIONSHIP_MAP.get(
                relation,
                relation.upper()
            )

    def normalize_events(self):
        for event in self.data["events"]:
            event["event_name"] = event["event_name"].strip()
            event_type = event["type"].lower()
            event["type"] = EVENT_TYPE_MAP.get(
                event_type,
                "UNKNOWN"
            )


    def normalize_confidence(self):

        for rel in self.data["relationships"]:
            rel["confidence_score"] = float(
                rel.get("confidence_score", 1.0)
            )

        for event in self.data["events"]:
            event["confidence_score"] = float(
                event.get("confidence_score", 1.0)
            )

    def remove_duplicate_entities(self):

        unique = {}

        for entity in self.data["entities"]:
            unique[entity["name"]] = entity

        self.data["entities"] = list(unique.values())