#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geocoding Automation Script
Written by Ernest Baker
For any questions or comments, contact: ernest_baker@example.com
"""

from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
import pandas as pd
import time

def geo(filename):
    """
    Geocode addresses from a CSV file using the Google Maps API.
    
    This function reads addresses from the 'Addy' column of a provided CSV file,
    geocodes them using the Google Maps API, and returns various geocoding details
    including latitude, longitude, and a comparison note between the provided and 
    found addresses. The results are written to an Excel file with a timestamped filename.
    """
    # Google API key (this should be stored securely in production environments)
    g = GoogleV3(api_key='YOUR_API_KEY_HERE')
    
    # Read the input CSV file
    df = pd.read_csv(filename)
    
    # Geocode addresses
    df['Geocode_Address'] = df['Addy'].apply(lambda x: g.geocode(x).address if g.geocode(x) else None)
    df['Latitude'] = df['Addy'].apply(lambda x: "{0:.7f}".format(g.geocode(x).latitude) if g.geocode(x) else None)
    df['Longitude'] = df['Addy'].apply(lambda x: "{0:.7f}".format(g.geocode(x).longitude) if g.geocode(x) else None)
    df['Lat_Long'] = df['Latitude'].map(str) + " " + df['Longitude'].map(str)
    
    # Clean and format data
    df['Lat_Long'] = df['Lat_Long'].str.replace('"', '')
    df.replace(to_replace=['TWP', 'Lane', 'United States'], value=['Township', 'LN', 'USA'], inplace=True)
    
    # Initialize 'Notes' column
    df['Notes'] = ''
    
    # Iterate over DataFrame to populate 'Notes' column
    for index, row in df.iterrows():
        lat_check = row['Latitude'].startswith("41") if row['Latitude'] else False
        long_check = row['Longitude'].startswith("-81") if row['Longitude'] else False
        address_check = row['Addy'].strip().lower() == row['Geocode_Address'].strip().lower() if row['Geocode_Address'] else False
        
        if lat_check and long_check and address_check:
            df.at[index, 'Notes'] = ''
        else:
            df.at[index, 'Notes'] = 'Review'
    
    # Format the output for Excel
    df['Latitude'] = df['Latitude'].apply(lambda x: f'"{x}"' if x else x)
    df['Longitude'] = df['Longitude'].apply(lambda x: f'"{x}"' if x else x)
    
    # Write the output to an Excel file
    output_filename = time.strftime(r'C:\Path\To\Geocode\%Y%m%dGeocodeIssues.xlsx')
    with pd.ExcelWriter(output_filename, mode='w', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Geocode Issues', index=False)
    
    quit()

if __name__ == '__main__':
    """
    The main loop attempts to run the geo function. 
    In case of a GeocoderTimedOut exception, it waits for 30 seconds and retries.
    If any other exception occurs, the script will print the error and exit.
    """
    while True:
        try:
            geo(r'C:\Path\To\Geocode\Lat_Long.csv')
        except GeocoderTimedOut:
            print("Geocoding timed out. Retrying in 30 seconds...")
            time.sleep(30)
        except Exception as err:
            print(f"An error occurred: {err}")
            quit()
