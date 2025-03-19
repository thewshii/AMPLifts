#!/usr/bin/env python3
"""
main.py - NEMT Scheduling CLI Gateway

On startup, this script fetches and displays scheduled rides (events) from Nylas,
then presents a menu to:
  a. Add a New Ride (interactive input)
  r. Refresh Scheduled Rides
  q. Quit

It uses Rich to display the rides and follows our initial wireframe.
"""

import time
from rich.console import Console
from rich.table import Table
from nylas import Client
from config import NYLAS_API_KEY, NYLAS_API_URI, NYLAS_GRANT_ID
from ride_sched import interactive_schedule_ride, parse_ride_event

def get_events_from_nylas():
    """
    Retrieves events from Nylas for the primary calendar.
    Uses the 'list()' method per Nylas docs.
    """
    try:
        nylas = Client(NYLAS_API_KEY, NYLAS_API_URI)
        # Retrieve events for the given grant id with query parameter for calendar_id.
        events = nylas.events.list(NYLAS_GRANT_ID, query_params={"calendar_id": "hawleywayne09@gmail.com"})
        return events
    except Exception as e:
        print("Error retrieving events:", e)
        return []

def display_scheduled_rides():
    console = Console()
    table = Table(title="Scheduled Rides")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Date", style="magenta")
    table.add_column("Member", style="magenta")
    table.add_column("Home (Pickup)", style="green")
    table.add_column("Doctor's Office", style="red")
    table.add_column("Status", style="yellow")
    table.add_column("Pickup Time", style="blue")
    table.add_column("Office Pickup", style="blue")

    events = get_events_from_nylas()
    if not events:
        console.print("No scheduled rides found.")
        return

    for event in events:
        ride = parse_ride_event(event)
        if ride is None:
            # Skip events that could not be parsed.
            continue
        table.add_row(
            str(ride["id"]),
            ride["date"],
            ride["member"],
            ride["home"],
            ride["doctor_office"],
            ride["status"],
            ride["pickup_time"],
            ride["office_pickup"]
        )
    console.print(table)

def main_menu():
    """
    Main menu acting as a gateway.
    Displays rides on startup, then loops to let the user add rides or refresh.
    """
    display_scheduled_rides()
    
    while True:
        print("\n--- NEMT Scheduling CLI ---")
        print("a. Add a New Ride")
        print("r. Refresh Scheduled Rides")
        print("q. Quit")
        choice = input("Select an option: ").strip().lower()
        if choice == "r":
            display_scheduled_rides()
        elif choice == "a":
            interactive_schedule_ride()
            display_scheduled_rides()
        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main_menu()
