class Relationship :
    def __init__(self, start_node, end_node, rel_type, confidence_score):
        self.source = start_node
        self.target = end_node
        self.rel_type = rel_type
        self.confidence_score = confidence_score

    def __repr__(self):
        return f"Relationship({self.source.name}, {self.rel_type}, {self.target.name})"