import os
import requests
import vobject
import caldav
import datetime 
import pytz
from caldav.elements import dav, cdav

def retrieve_broadcaster_schedule(broadcaster_id, access_token, client_id):
    url = f'https://api.twitch.tv/helix/schedule?broadcaster_id={broadcaster_id}'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-ID': client_id
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Assuming the response is JSON
            data = response.json()
            if 'data' in data:
                return data['data']['segments']
            else:
                print(f"No schedule data found for broadcaster {broadcaster_id}")
                return None
        else:
            print(f"Failed to retrieve schedule for broadcaster {broadcaster_id}: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred while retrieving schedule: {e}")
        return None

def parse_datetime(datetime_str):
    # Parse datetime string to a datetime object with timezone information
    naive_datetime = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    aware_datetime = pytz.utc.localize(naive_datetime)  # Assume UTC timezone
    return aware_datetime

def create_event(stream):
    # Parse start time and end time strings to datetime objects
    start_time = parse_datetime(stream['start_time'])
    end_time = parse_datetime(stream['end_time'])

    # Create a new iCalendar object
    cal = vobject.iCalendar()

    # Create a new event
    event = cal.add('vevent')

    # Set event properties based on the stream data
    event.add('summary').value = stream['title']
    event.add('dtstart').value = start_time
    event.add('dtend').value = end_time
    event.add('description').value = stream['title']
    event.add('location').value = 'Online'

    # Add a reminder
    alarm = event.add('valarm')
    alarm.add('action').value = 'DISPLAY'
    alarm.add('description').value = 'Event Reminder'
    alarm.add('trigger').value = datetime.timedelta(minutes=-10)

    return cal.serialize()

def delete_calendar(): 
    try:
        NEXTCLOUD_URL = os.getenv('NEXTCLOUD_URL')
        USERNAME = os.getenv('USERNAME')
        PASSWORD = os.getenv('PASSWORD')

        client = caldav.DAVClient(url=NEXTCLOUD_URL, username=USERNAME, password=PASSWORD)
        principal = client.principal()

        # Get the calendar to which the event will be added
        CALENDAR_NAME = os.getenv('CALENDAR_NAME')
        calendar = principal.calendar(name=CALENDAR_NAME)
        all_events = calendar.events()
        
        for event in all_events:
            event.delete()
            
        print("All events deleted from Nextcloud!")
            
    except Exception as e:
        print(f"Error uploading event to Nextcloud: {e}")

def upload_event_to_nextcloud(event):
    try:
        # Connect to Nextcloud CalDAV server
        NEXTCLOUD_URL = os.getenv('NEXTCLOUD_URL')
        USERNAME = os.getenv('USERNAME')
        PASSWORD = os.getenv('PASSWORD')
        
        client = caldav.DAVClient(url=NEXTCLOUD_URL, username=USERNAME, password=PASSWORD)
        principal = client.principal()

        # Get the calendar to which the event will be added
        CALENDAR_NAME = os.getenv('CALENDAR_NAME')
        calendar = principal.calendar(name=CALENDAR_NAME)

        # Add the event to the calendar
        if calendar:
            calendar.add_event(event)
            print("Event uploaded successfully to Nextcloud!")
        else:
            print("Calendar not found on Nextcloud.")
    except Exception as e:
        print(f"Error uploading event to Nextcloud: {e}")

def main():
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    CLIENT_ID = os.getenv('CLIENT_ID')
    TWITCH_CHANNELS = os.getenv('TWITCH_CHANNELS').split(',')
    STREAM_LIMIT = int(os.getenv('STREAM_LIMIT'))
    NEXTCLOUD_URL = os.getenv('NEXTCLOUD_URL')
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')


    delete_calendar()
    for channel in TWITCH_CHANNELS:
        schedule = retrieve_broadcaster_schedule(channel, ACCESS_TOKEN, CLIENT_ID)
        
        if schedule:
            for stream in schedule[:STREAM_LIMIT]:
                event = create_event(stream)
                upload_event_to_nextcloud(event)

if __name__ == "__main__":
    main()
