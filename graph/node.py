import uuid

class Node:
    def __init__(self, name, entity_type):
        self.id = str(uuid.uuid4())
        self.name = name
        self.entity_type = entity_type
        self.properties = {}


    def __repr__(self):
        return f"Node({self.name},{self.entity_type})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "entity_type": self.entity_type,
            "properties": self.properties
        }
    
    @classmethod
    def from_dict(cls, data):
        node = cls(data["name"], data["entity_type"])
        node.id = data["id"]
        node.properties = data.get("properties", {})
        return node