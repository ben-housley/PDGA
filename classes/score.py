from utilities.api_call import make_api_call_get
from classes.hole_score import HoleScore
from classes.round import Round
import pickle
import os

hole_breakdown_base = "https://www.pdga.com/api/v1/feat/live-scores/{}/hole-breakdowns" # Insert Score_ID
round_stat_base = "https://www.pdga.com/api/v1/feat/live-scores/{}/round-stats" # Insert Score_ID 
strokes_gained_base = "https://www.pdga.com/api/v1/feat/stats/strokes-gained/{}" # Insert Round_ID

class Score:
    # Initialized from the Result object
    def __init__(self, data):
        # Mandatory Fields
        self.score_id = data.get("ScoreID", None)
        self.player_name = data.get("player_name", None)
        self.player_pdga = data.get("player_pdga", None)
        self.layout_id = None # TODO Figure out course and layout IDs
        self.course_id = None
        self.result_id = None
        self.division = data.get("division", None)
        self.event_id = data["event_id"]
        self.round = data["Round"]
        self.tee_time = data["TeeTime"]
        self.starting_tee = data["TeeStart"]
        self.round_score = data["RoundScore"]
        self.total_score_to_par = data["ScoreToPar"]
        self.round_score_to_par = data["RoundToPar"]
        self.birdies = data["Birdies"]
        self.birdie_holes = data["BirdieHoles"]
        self.bogeys = data["Bogeys"]
        self.bogey_holes = data["BogeyHoles"]
        self.is_hot_round = data["HotRound"]
        self.is_round_complete = data["RoundComplete"]
        self.round_rating = data["RoundRating"]
        self.all_hole_scores = data["HoleScores"]
        self.layout = data["Layout"]

        # Fields that will be filled out later
        self.driving_hit = None
        self.driving_opp = None
        self.driving = None
        self.c1_reg_hit = None
        self.c1_reg_opp = None
        self.c1_reg = None 
        self.c2_reg_hit = None
        self.c2_reg_opp = None
        self.c2_reg = None 
        self.parked_hit = None
        self.parked_opp = None
        self.parked = None 
        self.scramble_hit = None
        self.scramble_opp = None
        self.scramble = None  
        self.c1x_putt_hit = None
        self.c1x_putt_opp = None
        self.c1x_putt = None 
        self.c2_putt_hit = None
        self.c2_putt_opp = None
        self.c2_putt = None 
        self.ob_hit = None
        self.ob_opp = None
        self.ob = None 
        self.birdie_hit = None
        self.birdie_opp = None
        self.birdie_rate = None 
        self.bogey_hit = None
        self.bogey_opp = None
        self.bogey_rate = None 
        self.double_bogey_plus_hit = None
        self.double_bogey_plus_opp = None
        self.double_bogey_plus_rate = None 
        self.par_hit = None
        self.par_opp = None
        self.par_rate = None 
        self.putting_total_dist = None  
        self.putting_long_dist = None 
        self.putting_avg_dist = None 
        self.avg_strokes = None

        self.sg_tee_to_green_rank = None
        self.sg_tee_to_green_opp = None
        self.sg_tee_to_green = None
        self.sg_c1x_rank = None
        self.sg_c1x_opp = None
        self.sg_c1x = None
        self.sg_c2_rank = None
        self.sg_c2_opp = None
        self.sg_c2 = None
        self.sg_putting_rank = None
        self.sg_putting_opp = None
        self.sg_putting = None

        # Methods to call on assignment
        self.get_round_details()
        self.get_hole_breakdown()
        self.get_round_stats()

    def get_round_details(self):
        round_details = Round.get_round_info(self.event_id, self.division, self.round)
        self.layout_id = round_details.layout_id
        self.round_id = round_details.round_id
        self.division_id = round_details.division_id
        self.get_strokes_gained()

    def get_hole_breakdown(self):
        hole_breakdown_path = hole_breakdown_base.format(self.score_id)
        breakdown = make_api_call_get(hole_breakdown_path).json()
        print("Pulling scores for round {} for player: {}".format(self.round, self.player_name))
        self.hole_scores = []
        for hole, score in self.all_hole_scores.items():
            details = self.layout["Detail"][hole]
            details["Score"] = score
            details["Hole"] = hole
            details["Round"] = self.round
            details["event_id"] = self.event_id
            details["layout_id"] = self.layout_id
            details["player_pdga"] = self.player_pdga
            for hole_breakdown in breakdown:
                if hole_breakdown["holeOrdinal"] == int(hole) and hole_breakdown["holeBreakdown"] is not None:
                    details.update(hole_breakdown["holeBreakdown"])

            self.hole_scores.append(HoleScore(details))
    
    
    def get_strokes_gained(self):
        strokes_gained_path = strokes_gained_base.format(self.round_id)
        if os.path.isfile("./strokes_gained_{}.pickle".format(self.round_id)):
            with open ("./strokes_gained_{}.pickle".format(self.round_id), 'rb') as f:
                strokes_gained = pickle.load(f)
        else: 
            strokes_gained = make_api_call_get(strokes_gained_path).json()
            with open("./strokes_gained_{}.pickle".format(self.round_id), 'wb') as f:
                pickle.dump(strokes_gained, f)
        for player in strokes_gained:
            if player["score"]["scoreId"] != self.score_id:
                continue
            self.result_id = player.get("score", None).get("resultId", None)
            for stat in player["stats"]:
                if stat["statId"] == 102:
                    self.sg_tee_to_green_rank = stat["rank"]
                    self.sg_tee_to_green_opp = stat["statOpportunityCount"]
                    self.sg_tee_to_green = stat["statValue"]
                if stat["statId"] == 104:
                    self.sg_c1x_rank = stat["rank"]
                    self.sg_c1x_opp = stat["statOpportunityCount"]
                    self.sg_c1x = stat["statValue"]
                if stat["statId"] == 105:
                    self.sg_c2_rank = stat["rank"]
                    self.sg_c2_opp = stat["statOpportunityCount"]
                    self.sg_c2 = stat["statValue"]
                # if stat["statId"] == 107:
                #     self.unknown_rank = stat["rank"]
                #     self.unknown_opp = stat["statOpportunityCount"]
                #     self.unknown = stat["statValue"]
                # if stat["statId"] == 103:
                #     self.unknown_rank = stat["rank"]
                #     self.unknown_opp = stat["statOpportunityCount"]
                #     self.unknown = stat["statValue"]
                # if stat["statId"] == 106:
                #     self.unknown_rank = stat["rank"]
                #     self.unknown_opp = stat["statOpportunityCount"]
                #     self.unknown = stat["statValue"]
                if stat["statId"] == 101:
                    self.sg_putting_rank = stat["rank"]
                    self.sg_putting_opp = stat["statOpportunityCount"]
                    self.sg_putting = stat["statValue"]
                # if stat["statId"] == 100:
                #     self.unknown_rank = stat["rank"]
                #     self.unknown_opp = stat["statOpportunityCount"]
                #     self.unknown = stat["statValue"]

    def get_round_stats(self):
        round_stats_path = round_stat_base.format(self.score_id)
        round_stats = make_api_call_get(round_stats_path).json()
        for stat in round_stats:
            if stat["statId"] == 1:
                self.driving_hit = stat["statCount"]
                self.driving_opp = stat["statOpportunityCount"]
                self.driving = stat["statValue"]
            elif stat["statId"] == 2:
                self.c1_reg_hit = stat["statCount"]
                self.c1_reg_opp = stat["statOpportunityCount"]
                self.c1_reg = stat["statValue"] 
            elif stat["statId"] == 3:
                self.c2_reg_hit = stat["statCount"]
                self.c2_reg_opp = stat["statOpportunityCount"]
                self.c2_reg = stat["statValue"] 
            elif stat["statId"] == 4:
                self.parked_hit = stat["statCount"]
                self.parked_opp = stat["statOpportunityCount"]
                self.parked = stat["statValue"] 
            elif stat["statId"] == 5:
                self.scramble_hit = stat["statCount"]
                self.scramble_opp = stat["statOpportunityCount"]
                self.scramble = stat["statValue"]  
            # elif stat["statId"] == 6:
            #     self.unknown_hit = stat["statCount"]
            #     self.unknown_opp = stat["statOpportunityCount"]
            #     self.unknown = stat["statValue"] 
            elif stat["statId"] == 7:
                self.c1x_putt_hit = stat["statCount"]
                self.c1x_putt_opp = stat["statOpportunityCount"]
                self.c1x_putt = stat["statValue"] 
            elif stat["statId"] == 8:
                self.c2_putt_hit = stat["statCount"]
                self.c2_putt_opp = stat["statOpportunityCount"]
                self.c2_putt = stat["statValue"] 
            elif stat["statId"] == 9:
                self.ob_hit = stat["statCount"]
                self.ob_opp = stat["statOpportunityCount"]
                self.ob = stat["statValue"] 
            elif stat["statId"] == 10:
                self.birdie_hit = stat["statCount"]
                self.birdie_opp = stat["statOpportunityCount"]
                self.birdie_rate = stat["statValue"] 
            elif stat["statId"] == 11:
                self.bogey_hit = stat["statCount"]
                self.bogey_opp = stat["statOpportunityCount"]
                self.bogey_rate = stat["statValue"] 
            elif stat["statId"] == 12:
                self.double_bogey_plus_hit = stat["statCount"]
                self.double_bogey_plus_opp = stat["statOpportunityCount"]
                self.double_bogey_plus_rate = stat["statValue"] 
            elif stat["statId"] == 13:
                self.par_hit = stat["statCount"]
                self.par_opp = stat["statOpportunityCount"]
                self.par_rate = stat["statValue"] 
            # elif stat["statId"] == 14:
            #     self.unknown_hit = stat["statCount"]
            #     self.unknown_opp = stat["statOpportunityCount"]
            #     self.unknown = stat["statValue"]  
            # elif stat["statId"] == 15:
            #     self.unknown_hit = stat["statCount"]
            #     self.unknown_opp = stat["statOpportunityCount"]
            #     self.unknown = stat["statValue"] 
            elif stat["statId"] == 16:
                self.putting_total_dist = stat["statValue"]  
            elif stat["statId"] == 17:
                self.putting_long_dist = stat["statValue"] 
            elif stat["statId"] == 18:
                self.putting_avg_dist = stat["statValue"] 
            elif stat["statId"] == 19:
                self.avg_strokes = stat["statValue"] 