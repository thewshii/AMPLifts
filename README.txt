# Ride Scheduling App

A self-managed ride scheduling application that integrates with the Nylas API for calendar events and the Google Maps API for address suggestions and geolocation. This app is designed for clients who will set up their own API credentials and grant IDs.

## Features

- **Calendar Event Creation:** Schedule rides by creating calendar events via Nylas.
- **Address Autocompletion:** Use the Google Maps Places Autocomplete API to suggest addresses.
- **Geocoding:** Convert addresses to latitude/longitude using the Google Maps Geocoding API.
- **Interactive CLI:** Schedule rides through an interactive command-line interface.

## Prerequisites

- **Python 3.7+** installed on your system.
- **pip** for installing Python packages.

## Required Accounts and API Keys

Before running the app, you need to set up the following:

1. **Google Cloud Account:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.
   - Enable the **Google Maps Places API** and **Geocoding API**.
   - Generate an API key (and restrict it as needed).
   - Copy the API key for later use.

2. **Nylas Account:**
   - Sign up for a new account at [Nylas](https://developer.nylas.com/).
   - Create a new application in the Nylas dashboard.
   - Obtain your **Nylas API Key** and **API URI**.
   - Create a **Grant ID** (this is needed to create calendar events via the API).
   - Copy these credentials for configuration.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <YOUR_REPO_URL>
   cd ride-scheduling-app

   Use the python command to run file after entering your unique API KEYS.

2. Set up a virtual environment

python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

## Usage
Running the Interactive Ride Scheduler
To run the interactive command-line interface for scheduling rides, execute:

- bash

python ride_sched.py
Follow the prompts to enter:

- Member Name
- Home (Pickup) Address
- Doctor's Office Address
- Date (in YYYY-MM-DD format)
- Status (e.g., Ambulatory or Wheelchair)
- Pickup Time (HH:MM; cannot be "WILLCALL")
- Office Pickup Time (HH:MM or type "WILLCALL")
- Testing Calendar Event Creation Directly
- To test creating a calendar event with preset values, run:

- bash

python nylas_api.py
This script will attempt to create an event using the test values defined in the file.

** Troubleshooting
Missing API Keys: Verify that the .env or config.py file exists and contains all required keys.

API Errors: Ensure that your API keys are active and that the required APIs are enabled in your Google Cloud and Nylas dashboards.

Grant ID Issues: Double-check that the Grant ID in your .env/config.py file matches the one provided by your Nylas account.
