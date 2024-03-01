from utilities.sql_db import sql_execute

db_name = "pdga_stats.db"

# Create event table
    # PK event_id - No FK
sql_execute(db_name, '''DROP TABLE IF EXISTS event''', 'drop')
event_query = ''' 
CREATE TABLE event(
    event_id INT PRIMARY KEY
    , start_date DATE
    , end_date DATE
    , total_players INT
    , name TEXT
    , simple_name TEXT
    , country TEXT
    , location TEXT
    , has_finals BOOLEAN
    , highest_completed_round INT
    , latest_round INT
    , final_round INT
    , tier TEXT
    , is_completed BOOLEAN
)
'''
sql_execute(db_name, event_query, 'create')


# Create division_event table
    # PK division_id 
    # FK event_id
sql_execute(db_name, '''DROP TABLE IF EXISTS division''', 'drop')
division_query = ''' 
CREATE TABLE division(
    division_id INT PRIMARY KEY
    , event_id INT
    , name TEXT
    , players INT
    , is_pro BOOLEAN
    , latest_round INT
    , FOREIGN KEY (event_id) REFERENCES event (event_id)
)
'''
sql_execute(db_name, division_query, 'create')


# Create round table
    # PK round_id
    # FK division_id
    # FK event_id 
    # FK layout_id 
sql_execute(db_name, '''DROP TABLE IF EXISTS round''', 'drop')
round_query = ''' 
CREATE TABLE round(
    round_id INT PRIMARY KEY
    , division_id INT
    , event_id INT
    , layout_id INT
    , pool TEXT
    , division TEXT
    , is_tee_time BOOLEAN
    , shotgun_time TEXT
    , FOREIGN KEY (division_id) REFERENCES division (division_id)
    , FOREIGN KEY (event_id) REFERENCES event (event_id)
    , FOREIGN KEY (layout_id) REFERENCES layout (layout_id)
)
'''
sql_execute(db_name, round_query, 'create')


# Create layout table
    # PK layout_id
    # FK course_id
    # FK event_id?
sql_execute(db_name, '''DROP TABLE IF EXISTS layout''', 'drop')
layout_query = ''' 
CREATE TABLE layout(
    layout_id INT PRIMARY KEY
    , course_id INT
    , event_id INT
    , course_name TEXT
    , name TEXT
    , num_holes INT
    , par INT
    , length REAL
    , units TEXT
    , accuracy TEXT
    , updated_date DATE
    , combined_ssa REAL
    , FOREIGN KEY (event_id) REFERENCES event (event_id)
)
'''
sql_execute(db_name, layout_query, 'create')


# Create event_results table
    # PK result_id
    # FK player_id (pdgaNum)
    # FK event_id
    # FK division_id NOT DOING, CAN GET FROM SCORE TABLE
sql_execute(db_name, '''DROP TABLE IF EXISTS event_result''', 'drop')
event_result_query = ''' 
CREATE TABLE event_result(
    result_id INT PRIMARY KEY
    , event_id INT
    , first_name TEXT
    , last_name TEXT
    , pdga_num INT
    , division TEXT
    , pool TEXT
    , place INT
    , place_rank INT
    , score NUMERIC
    , is_tied BOOLEAN
    , payout REAL
    , is_dnf BOOLEAN
    , total_strokes INT
    , name TEXT
    , average_round_rating INT
    , rating INT
    , rating_effective_date DATE
    , FOREIGN KEY (event_id) REFERENCES event (event_id)
)
'''
sql_execute(db_name, event_result_query, 'create')


# Create score table
    # PK score_id
    # FK player_id (pdgaNum)
    # FK event_id
    # FK layout_id 
    # FK round_id 
    # FK division_id
    # FK result_id
sql_execute(db_name, '''DROP TABLE IF EXISTS score''', 'drop')
score_query = ''' 
CREATE TABLE score(
    score_id INT PRIMARY KEY
    , player_name TEXT
    , player_pdga INT
    , layout_id INT
    , result_id INT
    , division TEXT
    , event_id INT
    , round INT
    , tee_time TEXT
    , starting_tee INT
    , round_score NUMERIC
    , total_score_to_par NUMERIC
    , round_score_to_par NUMERIC
    , birdies INT
    , birdie_holes INT
    , bogeys INT
    , bogey_holes INT
    , is_hot_round BOOLEAN
    , is_round_complete BOOLEAN
    , round_rating INT
    , round_id INT
    , division_id INT
    , driving_hit INT
    , driving_opp INT
    , driving REAL
    , c1_reg_hit INT
    , c1_reg_opp INT
    , c1_reg REAL
    , c2_reg_hit INT
    , c2_reg_opp INT
    , c2_reg REAL
    , scramble_hit INT
    , scramble_opp INT
    , scramble REAL
    , c1x_putt_hit INT
    , c1x_putt_opp INT
    , c1x_putt REAL
    , c2_putt_hit INT
    , c2_putt_opp INT
    , c2_putt REAL
    , ob_hit INT
    , ob_opp INT
    , ob REAL
    , birdie_hit INT
    , birdie_opp INT
    , birdie_rate REAL
    , bogey_hit INT
    , bogey_opp INT
    , bogey_rate REAL
    , double_bogey_plus_hit INT
    , double_bogey_plus_opp INT
    , double_bogey_plus_rate REAL
    , par_hit INT
    , par_opp INT
    , par_rate REAL
    , putting_total_dist REAL
    , putting_long_dist REAL
    , putting_avg_dist REAL
    , avg_strokes REAL
    , sg_tee_to_green_opp INT
    , sg_tee_to_green REAL
    , sg_tee_to_green_rank INT
    , sg_c1x_opp INT
    , sg_c1x REAL
    , sg_c1x_rank INT
    , sg_c2_opp INT
    , sg_c2 REAL
    , sg_c2_rank INT
    , sg_putting_opp INT
    , sg_putting REAL
    , sg_putting_rank INT

    , FOREIGN KEY (event_id) REFERENCES event (event_id)
    , FOREIGN KEY (layout_id) REFERENCES layout (layout_id)
    , FOREIGN KEY (round_id) REFERENCES round (round_id)
    , FOREIGN KEY (division_id) REFERENCES division (division_id)
    , FOREIGN KEY (result_id) REFERENCES event_result(result_id)
)
'''
sql_execute(db_name, score_query, 'create')

# Create player table?
    # PK player_id (pdgaNum)

# Create hole_score table
    # PK (hole_num, round_id, player_id) or (hole_num, round_num, player_id, event_id)
    # FK event_id
    # FK layout_id
sql_execute(db_name, '''DROP TABLE IF EXISTS hole_score''', 'drop')
hole_score_query = ''' 
CREATE TABLE hole_score(
    hole_num INT 
    , label TEXT
    , par INT
    , length REAL
    , score INT
    , driving TEXT
    , scramble TEXT
    , green TEXT
    , c1x INT
    , c1 INT
    , c2 INT
    , throw_in_dist REAL
    , ob INT
    , hazard INT
    , penalty INT
    , layout_id INT
    , round INT
    , event_id INT
    , player_pdga INT

    , PRIMARY KEY (hole_num, round, player_pdga, event_id)
    , FOREIGN KEY (event_id) REFERENCES event (event_id)
    , FOREIGN KEY (layout_id) REFERENCES layout (layout_id)
)
'''
sql_execute(db_name, hole_score_query, 'create')
