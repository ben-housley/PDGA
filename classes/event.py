from classes.division import Division
from classes.layout import Layout
from classes.round import Round
from classes.result import Result
from utilities.api_call import make_api_call_get

# event_id = "78651"
event_base = "https://www.pdga.com/apps/tournament/live-api/live_results_fetch_event?TournID={}" # Insert Tournament ID (Event ID)


class Event:
    def __init__(self, data):
        # Mandatory Fields
        self.event_id = data["TournamentId"]
        self.start_date = data["StartDate"]
        self.end_data = data["EndDate"]
        self.total_players = data["TotalPlayers"]
        self.name = data["Name"]
        self.simple_name = data["SimpleName"]
        self.country = data["Country"]
        self.location = data["Location"]
        self.has_finals = data["Finals"]
        self.highest_completed_round = data["HighestCompletedRound"]
        self.latest_round = data["LatestRound"]
        self.final_round = data["FinalRound"]
        self.tier = data["Tier"]

        # Calculated Fields
        self.is_completed = self.final_round = self.latest_round

        # Methods to call on assignment
        
        # self.all_layouts = data["Layouts"] # Better information for layouts exists on the round data
        self.all_divisions = data["Divisions"]

        self.get_divisions()
        self.get_mpo_rounds()
        self.get_results()
        # self.get_layouts()

    def get_divisions(self):
        self.divisions = []
        for division in self.all_divisions:
            self.divisions.append(Division(division, self.event_id))

    def get_layouts(self):
        self.layouts = []
        for layout in self.all_layouts:
            self.layouts.append(Layout(layout))

    def get_mpo_rounds(self):
        self.rounds = []
        for i in range(1, self.highest_completed_round + 1):
            self.rounds.append(Round.get_round_info(self.event_id, "MPO", i))

    def get_results(self):
        self.results = []
        for score in self.rounds[self.highest_completed_round-1].all_scores:
            self.results.append(Result.get_result_info(score["ResultID"]))


    def get_event_info(event_id):
        event_path = event_base.format(event_id)
        response = make_api_call_get(event_path).json()
        return Event(response["data"])