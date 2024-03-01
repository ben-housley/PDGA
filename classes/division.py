class Division:
    def __init__(self, data, event_id):
        # Initiated from Event object
        # Mandatory Fields
        self.division_id = data["DivisionID"]
        self.name = data["DivisionName"]
        self.players = data["Players"]
        self.layout_assignments = data["LayoutAssignments"]
        self.is_pro = data["IsPro"]
        self.latest_round = data["LatestRound"]
        self.event_id = event_id
        
        # Optional Fields
