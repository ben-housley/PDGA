class HoleScore():
    def __init__(self, data):
        # Initialized from Score object
        # Mandatory Fields
        self.hole_num = data.get("Hole", None)
        self.label = data.get("Label", None)
        self.par = data.get("Par", None)
        self.length = data.get("Length", None)
        self.score = data.get("Score", None)
        self.driving = data.get("driving", None)
        self.scramble = data.get("scramble", None) 
        self.green = data.get("green", None)
        self.c1x = data.get("c1x", None)
        self.c1 = data.get("c1", None)
        self.c2 = data.get("c2", None)
        self.throw_in_dist = data.get("throwIn", None)
        self.ob = data.get("ob", None)
        self.hazard = data.get("hazard", None)
        self.penalty = data.get("penalty", None)
        self.player_pdga = data.get("player_pdga", None)
        self.layout_id = data.get("layout_id", None)
        self.round = data["Round"]
        self.event_id = data["event_id"]