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
    
    df = pd.DataFrame(records)
    df = df[['city', 'timestamp', 'temperature', 'wind_speed', 'humidity', 'feels_like']] 
    df.columns = ['City','Time', 'Temperature (°C)', 'Wind Speed (km/h)', 'Humidity (%)', 'Feels Like (°C)']

    df[['Temperature (°C)', 'Wind Speed (km/h)', 'Humidity (%)', 'Feels Like (°C)']] = df[
    ['Temperature (°C)', 'Wind Speed (km/h)', 'Humidity (%)', 'Feels Like (°C)']
    ].round(1)

   
    fig, ax = plt.subplots(figsize=(12, len(df) * 0.7 + 1)) 
    ax.axis('off')

    plt.title("Weather Data Summary", fontsize=16, fontweight='bold', pad=20)

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

    table.auto_set_column_width([0, 1, 2, 3, 4, 5])

    output_path = "weather_summary_table.png"
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1)
    print(f"[✓] Weather summary table saved as {output_path}")

if __name__ == "__main__":
    cities = []
    visualise_weather_data(cities)
            

    

       
        