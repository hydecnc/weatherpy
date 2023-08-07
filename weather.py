from requests_html import HTMLSession
from geopy.geocoders import Nominatim
import subprocess

def get_weather(date: str = "today", location: str = "", unit: str = "c") -> str:
    """gets tempreature of given location (at given) in the provided unit

    Args:
        date (str, optional): date provided in mm/dd/yyyy. Defaults to "today".
        location (str, optional): location such as "New York". Defaults to "".
        unit (str, optional): celcius or farenheit. Defaults to "c".

    Returns:
        str: _description_
    """
    session = HTMLSession()

    location = get_loc(location)
    print(location)
    url = f"https://weather.com/weather/today/l/{location}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Langauge": "en-US,en;q=0.9",
    }
    params = {
        "unit": "m" if unit == "c" else "e",
    }

    results = session.get(
        url,
        headers=headers,
        params=params,
    )
    
    temperature = results.html.find("span.CurrentConditions--tempValue--MHmYY", first=True).text
    return temperature

def get_loc(location: str = "") -> str:
    """Get user's current location using curl if a location is not defined

    Args:
        location (str, optional): location from user. Defaults to "".

    Returns:
        str: location in a form of "lat,long"
    """
    if location == "":
        loc = subprocess.run(["curl", "ipinfo.io/loc"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        return loc
    
    geolocator = Nominatim(user_agent="MyApp")
    loc = geolocator.geocode(location)
    return f"{loc.latitude},{loc.longitude}"