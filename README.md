# weatherpy
Weather command line utility written in python

![](./demo.mp4)


```
Usage: main.py [OPTIONS]

 Get weather of the desired location, date range, and units.
 Defaults to today's weather in user location in celcius.

Options: 
--date                -d      TEXT  Date range of the weather. [default: today]
--location            -l      TEXT  The desired locaiton of the weather. Deafults to user's ip location if not provided.
--unit                -u      TEXT  Unit of the weather (celcius/farenheit). [default: c].
--verbose             -v            Get more information (High / Low, Wind, Humidity, Dew Point, Pressure, UV Index, Visibility, Moon Phase).
--help                              Show this message and exit.
```
