from classes.layout import Layout
from utilities.api_call import make_api_call_get

round_base = "https://www.pdga.com/apps/tournament/live-api/live_results_fetch_round?TournID={}&Division={}&Round={}"

class Round:
    def __init__(self, data):
        # Mandatory Fields
        self.pool = data["pool"]
        self.division = data["division"]
        self.id = data["live_round_id"]
        self.is_tee_time = data["tee_times"]
        
        # Optional Fields
        self.shotgun_time = data.get("shotgun_time", None)
        self.all_layouts = data.get("layouts", None)
        
        # Methods to call on assignment
        self.get_layouts()

    def get_layouts(self):
        self.layouts = []
        for layout in self.all_layouts:
            self.layouts.append(Layout(layout))
        
    def get_round_info(event_id, division="MPO", round=1):
        round_path = round_base.format(event_id, division, str(round))
        response = make_api_call_get(round_path).json()
        print(response)
        return Round(response["data"])