from .node import Node
from .relationship import Relationship

class Graph:
    def __init__(self):
        self.nodes = {}
        self.relationships = []

    def add_node(self, node_name, node_type):
        if node_name not in self.nodes:
            self.nodes[node_name] = Node(node_name, node_type)
        return self.nodes[node_name]

    def add_relationship(self, start_node_name, end_node_name, rel_type, confidence_score):
        start_node = self.nodes.get(start_node_name)
        end_node = self.nodes.get(end_node_name)

        if start_node and end_node:
            rel = Relationship(start_node, end_node, rel_type, confidence_score)
            self.relationships.append(rel)
            return rel
        else:
            raise ValueError("Both nodes must exist in the graph to create a relationship.")

    def find_node(self, node_name):
        return self.nodes.get(node_name, None)
    
    def get_outgoing_relationships(self, node):
        return [rel for rel in self.relationships if rel.source == node]

    def display_graph(self):
        for node_obj in self.nodes.values():
            print(f"Node: {node_obj.name}")
            node_relationships = self.get_outgoing_relationships(node_obj)
            for rel in node_relationships:
                print("|")
                print(f"--({rel.rel_type})--> {rel.target.name}")