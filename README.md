# Weather-Data-Pipeline

This is an ETL pipeline which uses Luigi to build and orchestrate the data pipeline. Goal of this pipeline is to fetch real time weather data, transformed as per the user's needs and
outputted to be visualised. 

Weather Data is fetched from OpenWeather API and WeatherAPI using GET REQUEST and then stored locally in JSON format. Transformed data is stored in an SQLite database. The final output 
data is merged from both API sources and then averaged to be visualised. 

Further enhancements to this project to be done: 

- Adding automatic scheduling to run at specific intervals (e.g., hourly or daily).

- Visualising data in a web application.
