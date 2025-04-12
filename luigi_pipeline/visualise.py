import pandas as pd
import sqlite3
import json
import os
from config import DB_PATH
import matplotlib.pyplot as plt

def visualise_weather_data(cities):

    records = []

    for city in cities:
         file_path = f'data/merged_and_averaged_{city}.json'
         if not os.path.exists(file_path):
              print(f"[!] No data found for {city} at {file_path}")
              continue
         
         with open(file_path, 'r') as f:
              data = json.load(f)
              data['city'] = city
              records.append(data)

    if not records:
        print("[!] No data available to visualize.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(records)
    df = df[['city', 'temperature', 'wind_speed', 'humidity', 'feels_like']]  # Clean column order
    df.columns = ['City', 'Temperature (°C)', 'Wind Speed (km/h)', 'Humidity (%)', 'Feels Like (°C)']

    df[['Temperature (°C)', 'Wind Speed (km/h)', 'Humidity (%)', 'Feels Like (°C)']] = df[
    ['Temperature (°C)', 'Wind Speed (km/h)', 'Humidity (%)', 'Feels Like (°C)']
    ].round(1)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, len(df) * 0.7 + 1))  # Dynamic height based on rows
    ax.axis('off')

    plt.title("Weather Data Summary", fontsize=16, fontweight='bold', pad=20)

    # Create the table
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc='center',
        cellLoc='center',
        colColours=['#f5f5f5'] * len(df.columns)
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    # Save as image
    output_path = "weather_summary_table.png"
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1)
    print(f"[✓] Weather summary table saved as {output_path}")

if __name__ == "__main__":
    cities = ['HELSINKI', 'LONDON', 'PARIS']
    visualise_weather_data(cities)
            

    

       
        