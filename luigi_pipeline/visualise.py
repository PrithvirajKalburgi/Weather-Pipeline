import pandas as pd
import sqlite3
import json
from config import DB_PATH
import matplotlib.pyplot as plt

def visualise_weather_data(city):

    DB_PATH = f'data/store_{city}_raw_data.db'

    try:
        conn = sqlite3.connect(DB_PATH)

        query = "SELECT * FROM weather_data WHERE city = ?"
        df = pd.read_sql(query, conn, params=(city,))
        conn.close()

        fig, ax = plt.subplots(figsize=(10, 4))  # Adjust the size as necessary
        ax.axis('off')  # Hide axes

            # Create the table and display it
        table = ax.table(cellText=df[['timestamp', 'temperature', 'wind_speed', 'humidity', 'feels_like']].values,
                            colLabels=['Timestamp', 'Temperature', 'Wind Speed', 'Humidity', 'Feels Like'],
                            loc='center', cellLoc='center', colColours=['#f5f5f5']*5)

            # Customize the table appearance (optional)
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)

            # Save the table as an image
        output_image_path = f"weather_data_table_{city}.png"
        plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0.05)

            # Show a success message
        print(f"Table for {city} saved as {output_image_path}")

    except sqlite3.OperationalError as e:
            print(f"Error: {e}")
            print(f"Could not find the database for {city} at {DB_PATH}")
        
if __name__ == "__main__":
    cities = ['HELSINKI', 'LONDON', 'PARIS']

    for city in cities:
        visualise_weather_data(city)

        