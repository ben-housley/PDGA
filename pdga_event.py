from classes.event import Event
import json 

event_id = "78651"
event_base = "https://www.pdga.com/apps/tournament/live-api/live_results_fetch_event?TournID="


# def get_event_info(event_id):
#     event_path = event_base + event_id
#     response = make_api_call_get(event_path).json()
#     new_event = Event(response["data"])
#     return new_event



waco_2023 = Event.get_event_info("66457")
print(vars(waco_2023))