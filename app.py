from extractor import extractor, text
from graph.graph import Graph
import json
from graph.normalizer import Normalizer
import os
from validator import Validator

extracted_Data= extractor(text)
data = json.loads(extracted_Data)

normalizer = Normalizer(data)
data = normalizer.normalize()

validator = Validator(data)

report = validator.validate()

report.print_report()

if report.passed:
    print("yay! All validations passed. Proceeding to graph construction...")
        
    # Add entities to the graph
    
    # Display the graph
    # graph.display_graph()
    # node_name_to_find = input("Enter the node name to find: ")
    # graph.find_node(node_name_to_find)

    # node_neighbours_to_find = input("Enter the node name to find neighbours for: ")
    # graph.find_neighbours(node_neighbours_to_find)

    # entity_type_to_find = input("Enter the entity type to find: ")
    # graph.find_by_type(entity_type_to_find)

    # relationship_type_to_find = input("Enter the relationship type to find: ")
    # graph.find_relationship(relationship_type_to_find)

    # path_to_find = input("Enter the starting node name for path finding: ")
    # target_node_name = input("Enter the target node name for path finding: ")
    # graph.find_path(path_to_find, target_node_name)

    file = "graph.json"
    if os.path.exists(file):
        graph = Graph.load(file)
    else:
        graph = Graph()

    graph.build_from_json(data)

    graph.save(file)

    # graph = Graph.load("graph.json")

    graph.display_graph()

else:
    print("Stop Graph Construction")

