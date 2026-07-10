import uuid

class Node:
    def __init__(self, name, entity_type):
        self.id = str(uuid.uuid4())
        self.name = name
        self.entity_type = entity_type
        self.properties = {}


    def __repr__(self):
        return f"Node({self.name},{self.entity_type})"