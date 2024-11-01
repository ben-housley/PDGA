import sqlite3
import json
from sanic import Sanic
from sanic import response
from utilities.sql_db import sql_execute
from pdga_event import update_db

app = Sanic("PDGA_Stats")

@app.before_server_start
async def attach_db(app, loop):
    app.ctx.db = sqlite3.connect("pdga_stats.db")

@app.route("/hello_world")
async def hello_world(request):
    return response.text("Hello, world.")

@app.route("/get_event_list")
async def get_event_list(request):
    query = '''SELECT event_id, name FROM event'''
    return response.json(json.dumps(sql_execute("pdga_stats.db", query, 'fetch')))

@app.route("/update_event")
async def update_event(request):
    try:
        event_id = request.args.get("event_id")
    except Exception as e:
        return response.text("ERROR: Missing request parameters")

    query = '''SELECT event_id FROM event'''
    event_list = sql_execute("pdga_stats.db", query, 'fetch')
    for record in event_list:
        if int(event_id) in record:
            return response.text("Event {} already exists in the database".format(event_id))
    try: 
        update_db(event_id)
    except Exception as e:
        return response.text(e)
    return response.text("Database updated successfully")

@app.route("/get_table")
async def get_table(request):
    #TODO Build out this route
    return response.text("ERROR: Missing request parameters")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)