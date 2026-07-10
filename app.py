from extractor import extractor, text
from graph.graph import Graph
import json


extracted_Data= extractor(text)
data = json.loads(extracted_Data)

graph = Graph()
graph_nodes = {}
    
# Add entities to the graph
for entity in data.get("entities", []):
    node_name = entity["name"]
    node_type = entity["type"]
    graph_nodes[node_name] = graph.add_node(node_name, node_type)

#Adding relationships to the graph
for rel in data.get("relationships", []):
    start_node_name = rel["entity_name1"]
    end_node_name = rel["entity_name2"]
    rel_type = rel["relationship_type"]
    confidence_score = rel.get("confidence_score", 1.0)  # Default confidence score to 1.0 if not provided

    # graph.add_relationship(start_node_name, end_node_name, rel_type, confidence_score)
    # print(f"Added relationship: {start_node_name} --({rel_type})--> {end_node_name} with confidence score {confidence_score}")

    try:
        graph.add_relationship(
            start_node_name,
            end_node_name,
            rel_type,
            confidence_score
        )
        print(f"✓ Added: {start_node_name} --{rel_type}--> {end_node_name}")

    except ValueError as e:
        print(f"✗ Failed: {start_node_name} --{rel_type}--> {end_node_name}")
        print(e)

# Display the graph
graph.display_graph()


