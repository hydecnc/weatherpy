from requests_html import HTMLSession
from geopy.geocoders import Nominatim
from rich.table import Table


class Weather:
    def __init__(self, location: str = "", unit: str = "c") -> None:
        self.session = HTMLSession()

        self.location = self.get_loc(location)
        print(f"Looking for weather at {self.location}")

        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Langauge": "en-US,en;q=0.9",
        }
        self.params = {
            "unit": "m" if unit == "c" else "e",
        }

    def get_weather(
        self, date: str = "today", month: bool = False, verbose: bool = False
    ) -> str | Table:
        """gets tempreature of given location (at given) in the provided unit

        Args:
            date (str, optional): date range of the weather. Defaults to "today".
            verbose (bool, optional): whether to get extra info (High / Low, Wind, Humidity, Dew Point, Pressure, UV Index, Visibility, Moon Phase) or not. Defaults to False.

        Returns:
            str: formatted string of the required data
        """
        if date == "today" and not month:
            return self.get_today_weather(verbose)
        else:
            return self.get_multiple_weathers(month, date)

    def get_today_weather(self, verbose: bool) -> str:
        """get today's weather

        Args:
            verbose (bool): verbose flag, if enabled gets extra information

        Returns:
            str: formatted string including all the data obtained
        """
        self.url = f"https://weather.com/weather/today/l/{self.location}"
        self.results = self.session.get(
            self.url,
            headers=self.headers,
            params=self.params,
        )
        temperature = self.results.html.find(
            "span.CurrentConditions--tempValue--MHmYY", first=True
        ).text
        feel_like_tempreature = self.results.html.find(
            "span.TodayDetailsCard--feelsLikeTempValue--2icPt", first=True
        ).text
        if verbose:
            other_data = self.get_extra_data()
            result = f"[bold red]Temperature :thermometer:[/bold red] {temperature}\n[bold red]Feels Like :thinking_face:[/bold red] {feel_like_tempreature}\n"
            for key, val in other_data.items():
                result += f"[bold red]{key}[/bold red]: {val}\n"
            return result
        else:
            return f"Temperature: {temperature}\nFeels Like: {feel_like_tempreature}"

    def get_multiple_weathers(self, month: bool, date: str) -> Table | str:
        self.url = f"https://weather.com/weather/monthly/l/{self.location}"
        self.results = self.session.get(
            self.url,
            headers=self.headers,
            params=self.params,
        )
        dates = self.results.html.find("span.CalendarDateCell--date--JO3Db")
        temperatures = self.results.html.find(
            "div.CalendarDateCell--temps--16oU1",
        )

        montly_data = {}
        for weekly_data in zip(dates, temperatures):
            montly_data[weekly_data[0].text] = weekly_data[1].text.replace("\n", "/")

        if month:
            montly_data = list(zip(montly_data.keys(), montly_data.values()))
            table = Table(
                "Sun",
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                show_lines=True,
                header_style="b red",
            )
            for i in range(5):
                weekly_data = []
                for data in montly_data[i * 7 : (i + 1) * 7]:
                    weekly_data.append(f"[bold green]{data[0]}[/bold green]: {data[1]}")
                table.add_row(*weekly_data)
            return table
        else:
            final_data = ""
            date_range = list(map(int, date.split("-")))

            for key, val in montly_data.items():
                if int(key) >= date_range[0] and int(key) <= date_range[1]:
                    final_data += f"[bold green]{key}[/bold green]: {val}\n"
            return final_data

    def get_extra_data(self) -> dict:
        """get extra data if verbose flag is used

        Returns:
            dict: dictionary containg the extra data
        """
        extra_data = {}
        extra_data_names = self.results.html.find(
            "div.WeatherDetailsListItem--label--2ZacS"
        )
        extra_data_values = self.results.html.find(
            "div.WeatherDetailsListItem--wxData--kK35q"
        )

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
