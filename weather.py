from requests_html import HTMLSession, HTMLResponse
from geopy.geocoders import Nominatim

session = HTMLSession()

def get_weather(
    date: str = "today", location: str = "", unit: str = "c", verbose: bool = False
) -> str:
    """gets tempreature of given location (at given) in the provided unit

    Args:
        date (str, optional): date range of the weather. Defaults to "today".
        location (str, optional): location ex) "New York". Defaults to "".
        unit (str, optional): unit either Celcius(c) or Farenheit(f). Defaults to "c".
        verbose (bool, optional): whether to get extra info (High / Low, Wind, Humidity, Dew Point, Pressure, UV Index, Visibility, Moon Phase) or not. Defaults to False.

    Returns:
        str: formatted string of the required data
    """

    location = get_loc(location)
    print(f"Looking for weather at {location}")

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

    temperature = results.html.find(
        "span.CurrentConditions--tempValue--MHmYY", first=True
    ).text
    feel_like_tempreature = results.html.find(
        "span.TodayDetailsCard--feelsLikeTempValue--2icPt", first=True
    ).text
    # other = results.html.find("div.TodayDetailsCard--detailsContainer--2yLtL", first=True).find("div")
    # for ot in other:
    #     print(ot.find("div"))
    if verbose:
        other_data = get_other_data(results)
        return f"Temperature: {temperature}\nFeels Like: {feel_like_tempreature}\nOther Data: {other_data}"
    else:
        return f"Temperature: {temperature}\nFeels Like: {feel_like_tempreature}"


def get_other_data(results: HTMLResponse) -> dict:
    """get extra data if verbose flag is used

    Args:
        results (HTMLResponse): the HTMLSession

    Returns:
        dict: dictionary of the extra data
    """
    other_data = {}
    other_data_names = results.html.find("div.WeatherDetailsListItem--label--2ZacS")
    other_data_values = results.html.find("div.WeatherDetailsListItem--wxData--kK35q")

    for data in zip(other_data_names, other_data_values):
        other_data[data[0].text] = data[1].text

    return other_data


def get_loc(location: str = "") -> str:
    """Get user's current location using curl if a location is not defined

    Args:
        location (str, optional): location from user. Defaults to "".

    Returns:
        str: location in a form of "lat,long"
    """
    if location == "":
        # loc = subprocess.run(["curl", "ipinfo.io/loc"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        loc = session.get("http://ipinfo.io/json").json()["loc"]
        return loc

    geolocator = Nominatim(user_agent="MyApp")
    loc = geolocator.geocode(location)
    return f"{loc.latitude},{loc.longitude}"
