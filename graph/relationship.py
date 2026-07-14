class Relationship :
    def __init__(self, start_node, end_node, rel_type, confidence_score):
        self.source = start_node
        self.target = end_node
        self.rel_type = rel_type
        self.confidence_score = confidence_score

    def to_dict(self):
        return {
            "source": self.source.name,
            "target": self.target.name,
            "relationship_type": self.rel_type,
            "confidence_score": self.confidence_score
        }

    def __repr__(self):
        return f"Relationship({self.source.name}, {self.rel_type}, {self.target.name})"
    
    @classmethod
    def from_dict(cls, data, graph):

        source = graph.find_node(data["source"])
        target = graph.find_node(data["target"])

        return cls(
            source,
            target,
            data["relationship_type"],
            data["confidence_score"]
        )