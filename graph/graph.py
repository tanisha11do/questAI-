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
    
    def get_incoming_relationships(self, node):
        return [rel for rel in self.relationships if rel.target == node]
    
    def get_outgoing_relationships(self, node):
        return [rel for rel in self.relationships if rel.source == node]
    
    def display_graph(self):
        for node_obj in self.nodes.values():
            print(f"\nNode: {node_obj.name}")
            print("-" * 40)

            # Incoming
            incoming = self.get_incoming_relationships(node_obj)
            print("Incoming Relationships:")

            if not incoming:
                print("  None")
            else:
                for rel in incoming:
                    print(f"  {rel.source.name} --[{rel.rel_type}]--> {node_obj.name}")

            # Outgoing
            outgoing = self.get_outgoing_relationships(node_obj)
            print("\nOutgoing Relationships:")

            if not outgoing:
                print("  None")
            else:
                for rel in outgoing:
                    print(f"  {node_obj.name} --[{rel.rel_type}]--> {rel.target.name}")

            print("-" * 40)

    # def display_graph(self):
    #     for node_obj in self.nodes.values():
    #         print(f"Node: {node_obj.name}")
    #         node_relationships = self.get_outgoing_relationships(node_obj)
    #         for rel in node_relationships:
    #             print("\n")
    #             print("Incoming Relationships:")
    #             if not rel:
    #                 print("None")
    #             else:
    #                 print(f"{rel.source.name} --[{rel.rel_type}]--> {rel.target.name}\n")
    #             # print(f"--({rel.rel_type})--> {rel.target.name}")

    #             print("Outgoing Relationships:")
    #             if not rel:
    #                 print("None")
    #             else:
    #                 print(f"{rel.source.name} --[{rel.rel_type}]--> {rel.target.name}\n")
    #             print("--------------------------------------------------")

