from utilities.api_call import make_api_call_get
from classes.score import Score

result_base = "https://www.pdga.com/apps/tournament/live-api/live_results_fetch_player?ResultID={}" # Insert Result_ID here

class Result:
    def __init__(self, data):
        # Initiated from Event object
        # Mandatory Fields
        self.result_id = data.get("ResultID", None)
        self.event_id = data.get("TournID", None)

        self.first_name = data["FirstName"]
        self.last_name = data["LastName"]
        self.pdga_num = data["PDGANum"]
        self.division = data["Division"]
        self.pool = data["Pool"]
        self.place = data["Place"]
        self.place_rank = data["PlaceRank"]
        self.score = data["ToPar"]
        self.is_tied = data["Tied"]
        self.payout = data.get("Prize", None)
        self.is_dnf = data["DNF"]
        self.total_strokes = data["Total"]
        self.name = data["Name"]
        self.average_round_rating = data["AverageRoundRating"]
        self.rating = data["Rating"]
        self.rating_effective_date = data["RatingEffectiveDate"]

        self.all_scores = data["Scores"]

        # Methods to call on assignment
        self.get_scores()

    def get_scores(self):
        self.scores = []
        for score in self.all_scores:
            score["event_id"] = self.event_id
            score["player_name"] = self.name
            score["player_pdga"] = self.pdga_num
            score["division"] = self.division
            score["result_id"] = self.result_id
            self.scores.append(Score(score))

    def get_result_info(result_id):
        result_path = result_base.format(result_id)
        response = make_api_call_get(result_path).json()
        return Result(response["data"])