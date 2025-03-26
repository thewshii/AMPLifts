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

   ```bash *ENTER IT ON THE CMD LINE*
   git clone https://github.com/thewshii/AMPLifts.git
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

To create your Grant ID with Nylas, you need to complete the OAuth flow, which connects your email account to your Nylas application. Here’s a step-by-step guide:

Log in to Your Nylas Dashboard:
Sign in at Nylas Developer and navigate to your application. If you haven’t created one yet, set up a new application to obtain your API credentials (client ID and client secret).

Set Up Your OAuth Configuration:
In your application settings, configure your OAuth settings by specifying a valid redirect URI. This URI should point to an endpoint in your app that handles OAuth callbacks (for example, http://localhost:5000/oauth/callback).

Initiate the OAuth Flow:
Run your app (or navigate to the appropriate endpoint in your deployed app). If you’re using the provided example, go to the /connect endpoint (e.g., http://localhost:5000/connect). This will redirect you to the Nylas authentication page.

Authenticate and Grant Permissions:
On the Nylas authentication page, sign in with your email provider and grant the requested permissions. This step authorizes your app to access the necessary data.

Receive the Grant ID:
Once you approve the authentication, you’ll be redirected back to your app’s OAuth callback URL. During this process, your app exchanges the authorization code for an access token. This access token acts as your Grant ID.

Save Your Grant ID:
Copy the access token (i.e., your Grant ID) from the OAuth callback’s response and add it to your .env file under the NYLAS_GRANT_ID variable.

By following these steps, you generate a Grant ID that securely connects your account to your Nylas application. If you encounter any issues, double-check your redirect URI and OAuth settings in the Nylas dashboard.