class Division:
    def __init__(self, data):
        # Mandatory Fields
        self.id = data["DivisionID"]
        self.name = data["DivisionName"]
        self.players = data["Players"]
        self.layout_assignments = data["LayoutAssignments"]
        self.is_pro = data["IsPro"]
        self.latest_round = data["LatestRound"]

        # Optional Fields
