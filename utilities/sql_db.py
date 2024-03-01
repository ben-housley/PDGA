import sqlite3

def sql_execute(db_name = "pdga_stats.db", query = '''SELECT * FROM INFORMATION''', result = 'create', vals = None):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    if result == 'insert':
        cursor.execute(query, vals)
    else:
        results = cursor.execute(query)

    if result == 'insert':
        results = conn.commit()
    elif result == 'fetch':
        results = cursor.fetchall()
    conn.close()
    return results
    


# c.execute('''CREATE TABLE IF NOT EXISTS event(eventID INT, name TEXT)''') # Create a new table

# event_id = 66457
# event_name = '2023 WACO'
# c.execute('''INSERT INTO event VALUES(?,?,?)''', (event_id, event_name))

# conn.commit() # Actually commit the new data to the database

# c.execute('''SELECT * FROM event''')
# results = c.fetchall() # Need to run this to get results of query
# print(results)


# c.execute('''DROP TABLE event''') # Drop the table

# conn.close()