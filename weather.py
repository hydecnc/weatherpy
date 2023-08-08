from requests_html import HTMLSession, HTMLResponse
from geopy.geocoders import Nominatim


class Weather:
    def __init__(self, location: str = "", unit: str = "c") -> None:
        self.session = HTMLSession()
        
        self.location = self.get_loc(location)
        print(f"Looking for weather at {self.location}")

        url = f"https://weather.com/weather/today/l/{self.location}"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Langauge": "en-US,en;q=0.9",
        }
        params = {
            "unit": "m" if unit == "c" else "e",
        }

        self.results = self.session.get(
            url,
            headers=headers,
            params=params,
        )

    def get_weather(
        self, date: str = "today", verbose: bool = False
    ) -> str:
        """gets tempreature of given location (at given) in the provided unit

        Args:
            date (str, optional): date range of the weather. Defaults to "today".
            verbose (bool, optional): whether to get extra info (High / Low, Wind, Humidity, Dew Point, Pressure, UV Index, Visibility, Moon Phase) or not. Defaults to False.

        Returns:
            str: formatted string of the required data
        """

        temperature = self.results.html.find(
            "span.CurrentConditions--tempValue--MHmYY", first=True
        ).text
        feel_like_tempreature = self.results.html.find(
            "span.TodayDetailsCard--feelsLikeTempValue--2icPt", first=True
        ).text

        if verbose:
            other_data = self.get_extra_data()
            return f"Temperature: {temperature}\nFeels Like: {feel_like_tempreature}\nOther Data: {other_data}"
        else:
            return f"Temperature: {temperature}\nFeels Like: {feel_like_tempreature}"


    def get_extra_data(self) -> dict:
        """get extra data if verbose flag is used

        Returns:
            dict: dictionary containg the extra data
        """
        extra_data = {}
        extra_data_names = self.results.html.find("div.WeatherDetailsListItem--label--2ZacS")
        extra_data_values = self.results.html.find("div.WeatherDetailsListItem--wxData--kK35q")

        for data in zip(extra_data_names, extra_data_values):
            if data[0].text == "Wind" or data[0].text == "Pressure":
                wanted_value = data[1].text.replace("\xa0", " ").split("\n")[1]
                extra_data[data[0].text] = wanted_value
                continue
            extra_data[data[0].text] = data[1].text

        return extra_data


    def get_loc(self, location: str = "") -> str:
        """Get user's current location using curl if a location is not defined

        Args:
            location (str, optional): location from user. Defaults to "".

        Returns:
            str: location in a form of "lat,long"
        """
        if location == "":
            # loc = subprocess.run(["curl", "ipinfo.io/loc"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
            loc = self.session.get("http://ipinfo.io/json").json()["loc"]
            return loc
        geolocator = Nominatim(user_agent="MyApp")
        loc = geolocator.geocode(location)
        return f"{loc.latitude},{loc.longitude}"
