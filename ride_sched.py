#!/usr/bin/env python3
"""
ride_sched.py - Scheduling Module for Rides

Provides functions to:
  - Get address suggestions using the Google Maps Places Autocomplete API.
  - Convert an address to lat/lng using the Google Maps Geocoding API.
  - Schedule a ride by creating a calendar event with Nylas.
  - Interactively prompt the user for ride details.

Before running:
  - Install packages: googlemaps, nylas, rich, prettytable.
    Example: pip install -U googlemaps nylas rich prettytable
  - Update API keys in config.py.
"""

import time
from prettytable import PrettyTable
from nylas import Client
from config import GOOGLE_API_KEY, NYLAS_API_KEY, NYLAS_API_URI, NYLAS_GRANT_ID

# Initialize googlemaps client.
import googlemaps
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

def get_place_suggestions(query):
    """
    Returns address suggestions via googlemaps.
    """
    try:
        suggestions = gmaps.places_autocomplete(query, types="address")
        return suggestions
    except Exception as e:
        print("Error retrieving place suggestions:", e)
        return []

def get_geolocation(address):
    """
    Returns (lat, lng) for a given address using googlemaps Geocoding.
    """
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return location['lat'], location['lng']
    except Exception as e:
        print("Error geocoding address:", e)
    return None, None

def convert_to_unix(date_str, time_str):
    """
    Converts date (YYYY-MM-DD) and time (HH:MM) to a Unix timestamp.
    Returns None if time_str is "WILLCALL".
    """
    if time_str.strip().upper() == "WILLCALL":
        return None
    combined = f"{date_str} {time_str}"
    struct_time = time.strptime(combined, "%Y-%m-%d %H:%M")
    return int(time.mktime(struct_time))

def schedule_ride(member, home, doctor_office, date, status, pickup_time_str, office_pickup_str):
    """
    Schedules a ride:
      - Validates and autocompletes addresses.
      - Converts date/time strings to Unix timestamps.
      - Creates a calendar event in Nylas.
    """
    # Validate and autocomplete addresses.
    home_suggestions = get_place_suggestions(home)
    doctor_suggestions = get_place_suggestions(doctor_office)
    home_address = home_suggestions[0]['description'] if home_suggestions else home
    doctor_address = doctor_suggestions[0]['description'] if doctor_suggestions else doctor_office

    # Get geolocation for logging.
    lat, lng = get_geolocation(home_address)
    print(f"DEBUG: Home address: {home_address} at lat: {lat}, lng: {lng}")
    
    # Convert times.
    start_time = convert_to_unix(date, pickup_time_str)
    end_time = convert_to_unix(date, office_pickup_str)
    if end_time is None and start_time is not None:
        end_time = start_time + 1800  # Default 30-minute duration

    # Initialize Nylas client.
    nylas = Client(NYLAS_API_KEY, NYLAS_API_URI)
    
    # Build event request.
    event_body = {
        "title": f"Ride for {member}",
        "location": home_address,
        "description": f"Pickup from {home_address} to {doctor_address}\nStatus: {status}",
        "when": {"start_time": int(start_time), "end_time": int(end_time)}
    }
    
    try:
        # Create event using grant id and specifying calendar_id.
        event_response = nylas.events.create(NYLAS_GRANT_ID, event_body, {"calendar_id": "hawleywayne09@gmail.com"})
        print("DEBUG: Nylas calendar event created successfully.")
    except Exception as e:
        print("Error creating Nylas event:", e)
    
    # Create and display a ride record.
    ride_data = {
        "id": 1,  # Demo: static ID
        "member": member,
        "home": home_address,
        "doctor_office": doctor_address,
        "date": date,
        "status": status,
        "pickup_time": time.strftime('%H:%M', time.localtime(start_time)) if start_time else "WILLCALL",
        "office_pickup": time.strftime('%H:%M', time.localtime(end_time)) if end_time else "WILLCALL"
    }
    pt = PrettyTable()
    pt.field_names = ["ID", "Member", "Home (Pickup)", "Doctor's Office", "Date", "Status", "Pickup Time", "Office Pickup"]
    pt.add_row([
        ride_data["id"], ride_data["member"], ride_data["home"],
        ride_data["doctor_office"], ride_data["date"], ride_data["status"],
        ride_data["pickup_time"], ride_data["office_pickup"]
    ])
    print(pt)
    return ride_data

def print_event_data(event):
    """
    Prints all the details of the event object for debugging purposes.
    """
    print("Event Data:")
    print(f"ID: {getattr(event, 'id', None)}")
    print(f"Title: {getattr(event, 'title', None)}")
    print(f"Location: {getattr(event, 'location', None)}")
    print(f"Description: {getattr(event, 'description', None)}")
    
    when_obj = getattr(event, 'when', None)
    if when_obj:
        print(f"Start Time: {getattr(when_obj, 'start_time', None)}")
        print(f"End Time: {getattr(when_obj, 'end_time', None)}")
    else:
        print("When: None")
    
    print(f"Participants: {getattr(event, 'participants', None)}")
    print(f"Read Only: {getattr(event, 'read_only', None)}")
    print(f"Busy: {getattr(event, 'busy', None)}")
    print(f"Status: {getattr(event, 'status', None)}")
    print(f"Calendar ID: {getattr(event, 'calendar_id', None)}")
    print(f"Recurrence: {getattr(event, 'recurrence', None)}")
    print(f"Master Event ID: {getattr(event, 'master_event_id', None)}")
    print(f"Original Start Time: {getattr(event, 'original_start_time', None)}")
    print(f"Owner: {getattr(event, 'owner', None)}")
    print(f"Organizer: {getattr(event, 'organizer', None)}")
    print(f"ICal UID: {getattr(event, 'ical_uid', None)}")
    print(f"Metadata: {getattr(event, 'metadata', None)}")
    
def parse_ride_event(event):
    """
    Parses a Nylas event object into a ride dictionary.

    Assumes events are created with:
      - title: "Ride for {member}"
      - location: Home (Pickup) address
      - description: "Pickup from {home} to {doctor_office}\nStatus: {status}"
      - when: an object with attributes start_time and end_time.
    
    Returns a dictionary with keys:
      id, date, member, home, doctor_office, status, pickup_time, office_pickup.
    If the event does not match expected format, returns None.
    """
    try:
        # Validate that event.title exists and is a string that starts with "Ride for "
        title = getattr(event, "title", None)
        print("DEBUG: Event title:", title)  # Debug print to see the title
        print_event_data(event)  # Debug print to see all event data
        if title is None:
            print("DEBUG: Title is None")
        elif not isinstance(title, str):
            print("DEBUG: Title is not a string")
        elif not title.startswith("Ride for "):
            print("DEBUG: Title does not start with 'Ride for '")
        
        if not isinstance(title, str) or not title.startswith("Ride for "):
            raise ValueError("Not a ride event (invalid title)")
        member = title.replace("Ride for ", "").strip()

        # Validate and get location
        home = getattr(event, "location", None)
        if not isinstance(home, str):
            raise ValueError("Invalid location")
        
        # Get description and parse doctor_office and status
        description = getattr(event, "description", "")
        doctor_office = ""
        status = ""
        if isinstance(description, str) and description:
            lines = description.split("\n")
            if lines and " to " in lines[0]:
                parts = lines[0].split(" to ")
                if len(parts) >= 2:
                    doctor_office = parts[1].strip()
            if len(lines) > 1:
                status = lines[1].replace("Status:", "").strip()
        
        # Get the 'when' object and retrieve start_time and end_time
        when_obj = getattr(event, "when", None)
        if when_obj is None:
            raise ValueError("Missing 'when' object")
        start_time = getattr(when_obj, "start_time", None)
        if start_time is None:
            raise ValueError("Missing start_time")
        end_time = getattr(when_obj, "end_time", None)
        
        date = time.strftime("%Y-%m-%d", time.localtime(start_time))
        pickup_time = time.strftime("%H:%M", time.localtime(start_time))
        office_pickup = time.strftime("%H:%M", time.localtime(end_time)) if end_time else "WILLCALL"
        
        return {
            "id": getattr(event, "id", ""),
            "date": date,
            "member": member,
            "home": home,
            "doctor_office": doctor_office,
            "status": status,
            "pickup_time": pickup_time,
            "office_pickup": office_pickup
        }
    except Exception as e:
        print("Error parsing an event:", e)
        return None

def interactive_schedule_ride():
    """
    Prompts the user for ride details (per our wireframe) and schedules the ride.
    Validates that Pickup Time is a valid HH:MM (cannot be "WILLCALL").
    """
    print("\n--- NEMT Ride Scheduler ---")
    member = input("Enter Member Name: ").strip()
    
    home = input("Enter Home (Pickup) Address: ").strip()
    suggestions = get_place_suggestions(home)
    if suggestions:
        print("Address suggestions:")
        for i, s in enumerate(suggestions, start=1):
            print(f"  {i}. {s['description']}")
        choice = input("Select a suggestion by number (or press Enter to keep your input): ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if index < len(suggestions):
                home = suggestions[index]['description']
    
    doctor_office = input("Enter Doctor's Office Address: ").strip()
    suggestions = get_place_suggestions(doctor_office)
    if suggestions:
        print("Address suggestions:")
        for i, s in enumerate(suggestions, start=1):
            print(f"  {i}. {s['description']}")
        choice = input("Select a suggestion by number (or press Enter to keep your input): ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if index < len(suggestions):
                doctor_office = suggestions[index]['description']
    
    date = input("Enter Date (YYYY-MM-DD): ").strip()
    status = input("Enter Status (Ambulatory or Wheelchair): ").strip()
    
    # Validate pickup time: it must be a valid HH:MM time, not "WILLCALL".
    while True:
        pickup_time_str = input("Enter Pickup Time (HH:MM): ").strip()
        if pickup_time_str.upper() == "WILLCALL":
            print("Error: Pickup Time cannot be 'WILLCALL'. Please enter a valid time in HH:MM format.")
        else:
            break
    
    # Office pickup time can be valid HH:MM or "WILLCALL".
    office_pickup_str = input("Enter Office Pickup Time (HH:MM) or type 'WILLCALL': ").strip()
    
    ride = schedule_ride(member, home, doctor_office, date, status, pickup_time_str, office_pickup_str)
    print("\nRide scheduled successfully!")
    return ride

# For testing purposes, you can run interactive_schedule_ride() directly:
if __name__ == "__main__":
    interactive_schedule_ride()
