from classes.event import Event
from utilities.sql_db import sql_execute
import pickle
import os

# TODO: Figure out the frontend app
# TODO: Figure out a way to have users input a tournament ID and if I don't already have stats for that tourney, then pull them
    # TODO: Include a loading bar when loading a new tournament's data
# TODO: Set up Sanic server w/ endpoints to interact with my DB (Robust backend)
# TODO: Identify what queries I want users to run against my DB? What data to display? What adds value beyond what PDGA has?
# TODO: Fix the scores class - it's not updating properly and last I ran it, there wasn't a score table?

# event_id = "78651" # 2024 All-Stars
# event_id = "66457" # 2023 WACO
# event_id = "77775" # 2024 Chess.com Florida
db_name = "pdga_stats.db"
events_to_update = ["77775"]
# waco_2023 = Event.get_event_info("66457")
# print(vars(waco_2023))

# Open a file for writing in binary mode.
# with open('waco.pickle', 'wb') as f:
    # Pickle the data to the file.
    # pickle.dump(waco_2023, f)

# Open the file for reading in binary mode.
# with open('waco.pickle', 'rb') as f:
# # #     # Unpickle the data from the file.
#     waco_2023 = pickle.load(f)

# Print the loaded data.
# print(vars(waco))

def update_db(event_id):
    if os.path.isfile("./{}.pickle".format(event_id)):
        with open ("./{}.pickle".format(event_id), 'rb') as f:
            evnt = pickle.load(f)
    else: 
        evnt = Event.get_event_info(event_id)
        with open("./{}.pickle".format(event_id), 'wb') as f:
            pickle.dump(evnt, f)

    vals_event = (evnt.event_id, evnt.start_date, evnt.end_data, evnt.total_players, evnt.name, 
        evnt.simple_name, evnt.country, evnt.location, evnt.has_finals, evnt.highest_completed_round,
        evnt.latest_round, evnt.final_round, evnt.tier, evnt.is_completed)
    query = '''INSERT INTO event VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    try: 
        sql_execute(db_name, query, 'insert', vals_event)
    except Exception as e:
        print("event error: {}".format(e))


    for division in evnt.divisions:
        vals_division = (division.division_id, division.event_id, division.name, division.players, division.is_pro, division.latest_round)
        query = '''INSERT INTO division VALUES(?,?,?,?,?,?)'''
        try:
            sql_execute(db_name, query, 'insert', vals_division)
        except Exception as e:
            print("division error: {}".format(e))


    for round in evnt.rounds:
        vals_round = (round.round_id, round.division_id, round.event_id, round.layout_id, round.pool, 
            round.division, round.is_tee_time, round.shotgun_time)
        query = '''INSERT INTO round VALUES(?,?,?,?,?,?,?,?)'''
        try:
            sql_execute(db_name, query, 'insert', vals_round)
        except Exception as e:
            print("round error: {}".format(e))



        for layout in round.layouts:
            vals_layout = (layout.layout_id, layout.course_id, layout.event_id, layout.course_name, 
                layout.name, layout.num_holes, layout.par, layout.length, layout.units,
                layout.accuracy, layout.updated_date, layout.combined_ssa)
            query = '''INSERT INTO layout VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'''
            try:
                sql_execute(db_name, query, 'insert', vals_layout)
            except Exception as e:
                print("layout error: {}".format(e))



    for result in evnt.results:
        vals_result = (result.result_id, result.event_id, result.first_name, result.last_name, result.pdga_num, 
            result.division, result.pool, result.place, result.place_rank, result.score, result.is_tied, 
            result.payout, result.is_dnf, result.total_strokes, result.name, result.average_round_rating,
            result.rating, result.rating_effective_date)
        query = '''INSERT INTO event_result VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        try: 
            sql_execute(db_name, query, 'insert', vals_result)
        except Exception as e:
            print("result error: {}".format(e))



        for score in result.scores:
            vals_score = (score.score_id, score.player_name, score.player_pdga, score.layout_id, score.result_id, 
                score.division, score.event_id, score.round, score.tee_time, score.starting_tee, score.round_score, 
                score.total_score_to_par, score.round_score_to_par, score.birdies, score.birdie_holes,
                score.bogeys, score.bogey_holes, score.is_hot_round, score.is_round_complete, 
                score.round_rating, score.round_id, score.division_id, score.driving_hit, score.driving_opp, score.driving,
                score.c1_reg_hit, score.c1_reg_opp, score.c1_reg, score.c2_reg_hit, score.c2_reg_opp, score.c2_reg,
                score.scramble_hit, score.scramble_opp, score.scramble, score.c1x_putt_hit, score.c1x_putt_opp, score.c1x_putt,
                score.c2_putt_hit, score.c2_putt_opp, score.c2_putt, score.ob_hit, score.ob_opp, score.ob, score.birdie_hit, 
                score.birdie_opp, score.birdie_rate, score.bogey_hit, score.bogey_opp, score.bogey_rate, score.double_bogey_plus_hit, 
                score.double_bogey_plus_opp, score.double_bogey_plus_rate, score.par_hit, score.par_opp, score.par_rate, score.putting_total_dist,
                score.putting_long_dist, score.putting_avg_dist, score.avg_strokes, score.sg_tee_to_green_opp, score.sg_tee_to_green, 
                score.sg_tee_to_green_rank, score.sg_c1x_opp, score.sg_c1x, score.sg_c1x_rank, score.sg_c2_opp, score.sg_c2, score.sg_c2_rank, 
                score.sg_putting_opp, score.sg_tee_to_green, score.sg_tee_to_green_rank)
            query = '''INSERT INTO score VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            try:
                sql_execute(db_name, query, 'insert', vals_score)
            except Exception as e:
                print("score error: {}".format(e))


            for hole_score in score.hole_scores:
                vals_hole_score = (hole_score.hole_num, hole_score.label, hole_score.par, hole_score.length, hole_score.score, 
                hole_score.driving, hole_score.scramble, hole_score.green, hole_score.c1x, hole_score.c1, hole_score.c2,
                hole_score.throw_in_dist, hole_score.ob, hole_score.hazard, hole_score.penalty, hole_score.layout_id,
                hole_score.round, hole_score.event_id, hole_score.player_pdga)
                query = '''INSERT INTO hole_score VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
                try:
                    sql_execute(db_name, query, 'insert', vals_hole_score)
                except Exception as e:
                    print("hole score error: {}".format(e))

if __name__ == '__main__':
    for event_id in events_to_update:
        update_db(event_id)