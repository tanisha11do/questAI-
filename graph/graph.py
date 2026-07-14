from collections import Counter
import json
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
            if rel not in self.relationships:
                self.relationships.append(rel)
                return rel
        else:
            raise ValueError("Both nodes must exist in the graph to create a relationship.")
    
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

    def find_node(self, name):
        if name in self.nodes:
            return self.nodes[name]
        else:
            raise ValueError(f"Node '{name}' does not exist in the graph.")
        
    def find_neighbours(self, node_name):
        neighbours = []
        for rel in self.relationships:
            if rel.source.name == node_name:
                neighbours.append(rel.target.name)
            elif rel.target.name == node_name:
                neighbours.append(rel.source.name)
            
        if neighbours:
            print(f"Neighbours of {node_name}: {', '.join(neighbours)}")
        else:
            print(f"No neighbours found for {node_name}.")

    def find_by_type(self,node_type):
        node_by_type = [node for node in self.nodes.values() if node.entity_type == node_type]
        print(f"{node_by_type}\n\n")
    
    def find_relationship(self,relation):
        edge = [rel for rel in self.relationships if rel.rel_type == relation]
        if edge:
            print(f"{edge}\n\n")
        else:
            print("No relations")

    def find_path(self, node1, node2):
        from collections import deque

        if node1 not in self.nodes or node2 not in self.nodes:
            raise ValueError("Both nodes must exist in the graph.")

        visited = set()
        queue = deque([(node1, [node1])])  # Store tuples of (current_node, path_to_current)

        while queue:
            current_node, path = queue.popleft()

            if current_node == node2:
                print(f"Path found: {' -> '.join(path)}\n\n")  # Return the path when the target node is found

            if current_node not in visited:
                visited.add(current_node)
                for rel in self.get_outgoing_relationships(self.nodes[current_node]):
                    next_node = rel.target.name
                    if next_node not in visited:
                        queue.append((next_node, path + [next_node]))

        return None  # Return None if no path is found

    def graph_summary(self):
        print("-" * 40)
        print("\nGraph Summary:\n\n")
        print(f"Total Nodes: {len(self.nodes)}\n")
        print(f"Total Relationships: {len(self.relationships)}\n")
        counts = Counter(
            node.entity_type.lower()
            for node in self.nodes.values()
        )

        for entity_type, count in sorted(counts.items()):
            print(f"Total {entity_type}s: {count}")
            print("-" * 40)

    def build_from_json(self,data):
        for entity in data.get("entities", []):
            node_name = entity["name"]
            node_type = entity["type"]
            self.add_node(node_name, node_type)

        #Adding relationships to the graph
        for rel in data.get("relationships", []):
            start_node_name = rel["entity_name1"]
            end_node_name = rel["entity_name2"]
            rel_type = rel["relationship_type"]
            confidence_score = rel.get("confidence_score", 1.0)  # Default confidence score to 1.0 if not provided

            # graph.add_relationship(start_node_name, end_node_name, rel_type, confidence_score)
            # print(f"Added relationship: {start_node_name} --({rel_type})--> {end_node_name} with confidence score {confidence_score}")

            try:
                self.add_relationship(
                    start_node_name,
                    end_node_name,
                    rel_type,
                    confidence_score
                )
                print(f"✓ Added: {start_node_name} --{rel_type}--> {end_node_name}")

            except ValueError as e:
                print(f"✗ Failed: {start_node_name} --{rel_type}--> {end_node_name}")
                print(e)

        for ev in data.get("events", []):
            event_name = ev["event_name"]

            # I recommend storing all events as type "Event"
            event_node = self.add_node(event_name, "Event")

            # Store event details as properties
            event_node.properties["event_type"] = ev["type"]
            event_node.properties["description"] = ev.get("description", "")
            event_node.properties["confidence"] = ev.get("confidence_score", 1.0)

            # Create a relationship between the event and its subject
            subject = ev.get("subject")

            if subject in self.nodes:
                self.add_relationship(subject, event_name, "TRIGGERS", confidence_score)
                print(f"✓ Added: {subject} --TRIGGERS--> {event_name}")
            else:
                print(f"✗ Failed: Subject '{subject}' for event '{event_name}' does not exist in the graph.")

    

    def save(self, filename):

        graph_data = {

            "nodes":[
                node.to_dict()
                for node in self.nodes.values()
            ],

            "relationships":[
                rel.to_dict()
                for rel in self.relationships
            ]
        }

        with open(filename, "w") as f:
            json.dump(graph_data, f, indent=4)

        print(f"Graph saved to {filename}")

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

    @classmethod
    def load(cls, filename):

        with open(filename) as f:
            graph_data = json.load(f)

        graph = cls()

        for node_data in graph_data["nodes"]:

            node = Node.from_dict(node_data)

            graph.nodes[node.name] = node

        for rel_data in graph_data["relationships"]:

            rel = Relationship.from_dict(rel_data, graph)

            graph.relationships.append(rel)

        return graph