from classes.layout import Layout
from utilities.api_call import make_api_call_get
import pickle
import os

round_base = "https://www.pdga.com/apps/tournament/live-api/live_results_fetch_round?TournID={}&Division={}&Round={}"

class Round:
    def __init__(self, data, event_id):
        # Initiated from get_round_info by Event object
        # Mandatory Fields
        self.pool = data["pool"]
        self.division = data["division"]
        self.round_id = data["live_round_id"]
        self.division_id = data["id"]
        self.is_tee_time = data["tee_times"]
        self.event_id = event_id
        
        # Optional Fields
        self.shotgun_time = data.get("shotgun_time", None)
        self.all_layouts = data.get("layouts", None)
        self.all_scores = data.get("scores", None)

        # Round Stat Fields - not set at initialization

        # Methods to call on assignment
        self.get_layouts()

    def get_layouts(self):
        self.layouts = []
        for layout in self.all_layouts:
            self.layouts.append(Layout(layout))
            self.layout_id = layout["LayoutID"] # If there are pools then this will only capture one of the layouts ...
        
    def get_round_info(event_id, division="MPO", round=1):
        round_path = round_base.format(event_id, division, str(round))
        if os.path.isfile("./round_{}_{}_{}.pickle".format(event_id, division, str(round))):
            with open ("./round_{}_{}_{}.pickle".format(event_id, division, str(round)), 'rb') as f:
                rnd = pickle.load(f)
        else: 
            rnd = make_api_call_get(round_path).json()
            with open("./round_{}_{}_{}.pickle".format(event_id, division, str(round)), 'wb') as f:
                pickle.dump(rnd, f)
        return Round(rnd["data"], event_id)
