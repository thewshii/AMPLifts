"""
nylas_api.py

This module handles calendar event creation using the Nylas Python SDK.
It initializes the Nylas client with your credentials (stored in your config or environment)
and exposes a helper function to create an event.
"""

import os
from nylas import Client  # Using the Nylas Python SDK (v6.x compatible with Nylas v3 APIs)
from config import NYLAS_API_KEY, NYLAS_API_URI  # Your config module that loads these from env

def create_calendar_event(title, location, description, start_time, end_time=None):
    """
    Creates a calendar event via the Nylas API.

    :param title: The title of the event (e.g., "Ride for Jane Doe")
    :param location: The event location (typically the Home Pickup address)
    :param description: A detailed description (including Doctor's Office, etc.)
    :param start_time: Unix timestamp for the pickup time (maps to the event's start_time)
    :param end_time: Unix timestamp for the office pickup time (maps to the event's end_time)
                     If None or if the user specifies "WILLCALL", the end_time is omitted.
    :return: The created event's ID or None if creation failed.
    """
    try:
        # Initialize the Nylas client using the credentials from your config/environment.
        nylas = Client(
            api_key=NYLAS_API_KEY,
            api_uri=NYLAS_API_URI
        )
        
        # Create a new calendar event.
        event = nylas.events.create()
        event.title = title
        event.location = location
        event.description = description
        
        # Set the event times: start_time is required; include end_time if provided.
        event.when = {"start_time": start_time}
        if end_time:
            event.when["end_time"] = end_time
        
        # Save the event to the calendar (this makes the API call to Nylas).
        event.save()
        print("Event created with ID:", event.id)
        return event.id
    except Exception as e:
        print("Error creating calendar event:", e)
        return None

# Example usage:
if __name__ == "__main__":
    import time
    # For demonstration: create an event starting 1 hour from now and ending 1.5 hours from now.
    current_time = int(time.time())
    pickup_time = current_time + 3600  # Home Pickup time (start time)
    office_pickup_time = current_time + 5400  # Office Pickup time (end time) -- or None for WILLCALL

    event_id = create_calendar_event(
        title="Ride for Jane Doe",
        location="123 Main St (Home Pickup)",
        description="Pickup from home; dropoff at doctor's office: 456 Elm St.",
        start_time=pickup_time,
        end_time=office_pickup_time  # Pass None if the customer opts for "WILLCALL"
    )
