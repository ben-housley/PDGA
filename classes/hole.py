class Hole:
    def __init__(self, data):
        # Mandatory Fields
        self.name = data.get("Hole", None)
        self.label = data.get("Label", None)
        self.par = data.get("Par", None)
        self.length = data.get("Length", None)

        # Optional Fields
        self.ordinal = data.get("Ordinal", None)
        self.units = data.get("Units", None)
        self.accuracy = data.get("Accuracy", None)