from utilities.sql_db import sql_execute

db_name = "pdga_stats.db"
query = '''
SELECT event_id, name, start_date, end_date, total_players
FROM event
WHERE start_date >= '2024-01-01'
'''
print(sql_execute(db_name, query, 'fetch'))