import json
import constants
from extractor import extractor,text
from graph import graph

# print(repr(extractor(text)))
data = json.loads(extractor(text))

class ValidationReport:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {
            "entities": 0,
            "relationships": 0,
            "events": 0
        }

    def add_error(self, message):
        self.errors.append(message)

    def add_warning(self, message):
        self.warnings.append(message)

    @property
    def passed(self):
        return len(self.errors) == 0

    def print_report(self):
        print("\n========== VALIDATION REPORT ==========")

        print(f"\nEntities      : {self.stats['entities']}")
        print(f"Relationships : {self.stats['relationships']}")
        print(f"Events        : {self.stats['events']}")

        if self.errors:
            print("\nERRORS")
            for error in self.errors:
                print(f"  ❌ {error}")

        if self.warnings:
            print("\nWARNINGS")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")

        if self.passed:
            print("\n✅ Validation Passed")
        else:
            print("\n❌ Validation Failed")

        print("=======================================\n")

class Validator:

    def __init__(self, data):
        self.data = data
        self.report = ValidationReport()

    def validate_schema(self):

        expected_schema = {
            "entities": list,
            "relationships": list,
            "events": list
        }

        for key, expected_type in expected_schema.items():

            if key not in self.data:
                self.report.add_error(f"Missing key '{key}'")
                continue

            if not isinstance(self.data[key], expected_type):
                self.report.add_error(
                    f"{key} should be {expected_type.__name__}"
                )
        if not self.report.errors:
            print("Schema validation passed. ✅")                

    def validate_entities(self):

        allowed = set(constants.ENTITY_TYPES)

        for entity in self.data.get("entities", []):

            self.report.stats["entities"] += 1

            if "name" not in entity:
                self.report.add_error("Entity missing name")
                continue

            if "type" not in entity:
                self.report.add_error(
                    f"{entity['name']} missing type"
                )
                continue

            if entity["type"] not in allowed:
                self.report.add_warning(
                    f"Unknown entity type '{entity['type']}'"
                )
        if not self.report.errors:
            print("Entity validation passed. ✅")

    def validate_relationships(self):

        allowed = set(constants.RELATIONSHIP_TYPES)

        for rel in self.data.get("relationships", []):

            self.report.stats["relationships"] += 1

            required = [
                "entity_name1",
                "relationship_type",
                "entity_name2"
            ]

            for field in required:

                if field not in rel:
                    self.report.add_error(
                        f"Relationship missing '{field}'"
                    )

            if rel.get("relationship_type") not in allowed:
                self.report.add_warning(
                    f"Unknown relationship '{rel.get('relationship_type')}'"
                )

        if not self.report.errors:
            print("Relationship validation passed. ✅")

    def validate_events(self):

        allowed = set(constants.EVENT_TYPES)

        for event in self.data.get("events", []):

            self.report.stats["events"] += 1

            required = [
                "event_name",
                "type",
                "subject",
                "description"
            ]

            for field in required:

                if field not in event:
                    self.report.add_error(
                        f"Event missing '{field}'"
                    )

            if event.get("type") not in allowed:
                self.report.add_warning(
                    f"Unknown event type '{event.get('type')}'"
                )

        if not self.report.errors:
            print("Event validation passed. ✅")

    def validate_graph_integrity(self):

        entity_names = {
            entity["name"]
            for entity in self.data.get("entities", [])
        }

        for rel in self.data.get("relationships", []):

            if rel["entity_name1"] not in entity_names:
                self.report.add_error(
                    f"Unknown entity '{rel['entity_name1']}'"
                )

            if rel["entity_name2"] not in entity_names:
                self.report.add_error(
                    f"Unknown entity '{rel['entity_name2']}'"
                )

        if not self.report.errors:
            print("Graph integrity validation passed. ✅")

    def validate_confidence(self):

        for rel in self.data.get("relationships", []):

            score = rel.get("confidence_score")

            if score is None:
                continue

            if score < 0.7:
                self.report.add_error(
                    f"Low confidence relationship ({score})"
                )

            elif score < 0.9:
                self.report.add_warning(
                    f"Medium confidence relationship ({score}) for relationship {rel['entity_name1']} --{rel['relationship_type']}--> {rel['entity_name2']}"
                )

        for event in self.data.get("events", []):

            score = event.get("confidence_score")

            if score is None:
                continue

            if score < 0.7:
                self.report.add_error(
                    f"Low confidence event ({score})"
                )

            elif score < 0.9:
                self.report.add_warning(
                    f"Medium confidence event ({score})"
                )

        if not self.report.errors:
            print("Confidence validation passed. ✅")

    def validate(self):

        self.validate_schema()
        self.validate_entities()
        self.validate_relationships()
        self.validate_events()
        self.validate_graph_integrity()
        self.validate_confidence()

        return self.report
    








# from extractor import extractor, text
# from graph.graph import Graph
# import json

# data = json.loads(extractor(text))

# def validate_schema():
#     expected_schema = {
#         "entities": list,
#         "relationships": list,
#         "events": list
#     }

#     for key, expected_type in expected_schema.items():
#         if key not in data:
#             print(f"Missing key: {key}")
#             return False
#         if not isinstance(data[key], expected_type):
#             print(f"Incorrect type for key: {key}. Expected {expected_type}, got {type(data[key])}")
#             return False
   
# def validate_entities():
#     for entity in data.get("entities", []):
#         if "name" not in entity or "type" not in entity:
#             print(f"Entity missing required fields: {entity}")
#             return False
    
# def validate_relationships():
#     for relationship in data.get("relationships", []):
#         if "entity_name1" not in relationship or "relationship_type" not in relationship or "entity_name2" not in relationship:
#             print(f"Relationship missing required fields: {relationship}")
#             return False

# def validate_events():   
#     for event in data.get("events", []):
#         if "event_name" not in event or "type" not in event or "subject" not in event or "description" not in event:
#             print(f"Event missing required fields: {event}")
#             return False       
        
# def graph_integrity():
#     for relationship in data.get("relationships", []):
#         entity_name1 = relationship.get("entity_name1")
#         entity_name2 = relationship.get("entity_name2")
#         if not any(entity.get("name") == entity_name1 for entity in data.get("entities", [])):
#             print(f"Entity {entity_name1} in relationship does not exist in entities.")
#             return False
#         if not any(entity.get("name") == entity_name2 for entity in data.get("entities", [])):
#             print(f"Entity {entity_name2} in relationship does not exist in entities.")
#             return False
        
# def validate_confidence_scores():
#     for relationship in data.get("relationships", []):
#         confidence_score = relationship.get("confidence_score")
#         if confidence_score is not None and (not isinstance(confidence_score, (int, float)) or not (0.7 <= confidence_score <= 1)):
#             print(f"Invalid confidence score for relationship: {relationship}")
#             return False
#     for event in data.get("events", []):
#         confidence_score = event.get("confidence_score")
#         if confidence_score is not None and (not isinstance(confidence_score, (int, float)) or not (0.7 <= confidence_score <= 1)):
#             print(f"Invalid confidence score for event: {event}")
#             return False
        
# def validation_report():
#     print("Validation Report:")
#     validation_checks = {
#         "Schema Validation": validate_schema,
#         "Entity Validation": validate_entities,
#         "Relationship Validation": validate_relationships,
#         "Event Validation": validate_events,
#         "Graph Integrity Validation": graph_integrity,
#         "Confidence Score Validation": validate_confidence_scores
#     }

#     all_passed = True
#     for validation_name, validation_func in validation_checks.items():
#         is_valid = validation_func()
#         if not is_valid:
#             print(f"{validation_name} failed.")
#             validation_func()
#             all_passed = False

#     if all_passed:
#         print("All validations passed successfully.")

# validation_report()
