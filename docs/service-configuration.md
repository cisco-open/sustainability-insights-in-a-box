# Configuring Microservices

Sustainability Insights microservices are preconfigured to with required values. Some settings can be chanhged through [docker-compose file](../docker-compose.yaml). This file describes only the important parameters. Also note that, all these changes require restart to take effect.

## Configuration Parameters

- Scheduler MS:
  In case a custom device inventory and collection configuration file is used, mounted is as below. Change  **only the source key** to point to the correct location.
  ```
    volumes:
    - type: bind
      target: /susit/scheduler/config.yaml
      source: ./config.yaml
  ```
- Processor MS:
  This solution can fetch latest CO2 Emission Intensity at a given location from [ElectricityMap API](https://static.electricitymaps.com/api/docs/index.html). Update `ENERGYMAP_KEY` environment variable with a valid key.

  If valid API key is not available, configure a default CO2 Emission Intensity value for the site in the inventory configuration file.

- Database:
  Solution uses a Postgres/Timescale database to store collected and calculated metrics. Set `DBUSER` and `DBPASS` environment variables to use any custom values. Do remember to apply exact same values for `processor` and `superset` services.

- Superset MS:
  By default, the formatting specifications for various types of data, such as numbers, dates, times, and currency symbols, are set to European style. To adjust these formatting specifications to adhere to a different style, modify the properties in the 'superset_config.py' file under the name 'D3_FORMAT'. 
  For example, for US style:
  ```
  D3_FORMAT = {
    "decimal": ".",
    "thousands": ",",
    "grouping": [3],
    "currency": ["£", ""],
    "dateTime": "%a %e %b %X %Y",
    "date": "%d/%m/%Y",
    "time": "%H:%M:%S",
    "periods": ["AM", "PM"],
    "days": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    "shortDays": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "shortMonths": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    }
  ```
