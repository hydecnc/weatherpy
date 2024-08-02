from geopy.geocoders import Nominatim
from rich.table import Table
import requests
import lxml.html
import lxml.cssselect
from rich.progress import Progress, SpinnerColumn, TextColumn


class Weather:
    def __init__(self, location: str = "", unit: str = "c") -> None:
        self.location = self.get_loc(location)

        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; HTMLLinux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Langauge": "en-US,en;q=0.9",
        }
        self.params = {
            "unit": "m" if unit == "c" else "e",
        }

    def get_weather(
        self, date: str = "today", month: bool = False, verbose: bool = False
    ) -> str | Table:
        """Gets tempreature of given location (at given) in the provided unit

        Args:
            date (str, optional): Date range of the weather. Defaults to "today".
            verbose (bool, optional): Whether to get extra info (High / Low, Wind, Humidity, Dew Point, Pressure, UV Index, Visibility, Moon Phase) or not. Defaults to False.

        Returns:
            str: Formatted string of the required data
        """
        if date == "today" and not month:
            return self.get_today_weather(verbose)
        else:
            return self.get_multiple_weathers(month, date)

    def get_content(self, url: str) -> requests.Response:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description=f"Looking for weather at {self.location}...", total=None
            )
            results = requests.get(url, headers=self.headers, params=self.params)

        if results.status_code != 200:
            raise Exception(
                f"Failed to retrieve information: {self.results.status_code}"
            )
        tree = lxml.html.fromstring(results.content)

        return tree

    def extract_content(
        self, tree: lxml.html.HtmlElement, selector: str, multiple: bool = False
    ) -> str | list:
        """Extracts content from the tree given using the selector.

        Args:
            tree (lxml.html.HtmlElement): HTML from a website
            selector (str): CSS selector used for extraction
            multiple (bool, optional): Option to make the function return a list of matches instead of the first match. Defaults to False.

        Returns:
            str | list: The content of first matc
        """

        selector = lxml.cssselect.CSSSelector(selector)
        if multiple:
            return [text.text_content() for text in selector(tree)]
        return selector(tree)[0].text_content()

    def get_today_weather(self, verbose: bool) -> str:
        """Get today's weather

        Args:
            verbose (bool): Verbose flag, if enabled gets extra information

        Returns:
            str: Formatted string including all the data obtained
        """
        url = f"https://weather.com/weather/today/l/{self.location}"
        tree = self.get_content(url)

        temperature = self.extract_content(
            tree, "span.CurrentConditions--tempValue--MHmYY"
        )
        feels_like_temperature = self.extract_content(
            tree, "span.TodayDetailsCard--feelsLikeTempValue--2icPt"
        )

        if verbose:
            other_data = self.get_extra_data(tree)
            return other_data
            result = f"[bold red]Temperature :thermometer:[/bold red] {temperature}\n[bold red]Feels Like :thinking_face:[/bold red] {feels_like_temperature}\n"
            for key, val in other_data.items():
                result += f"[bold red]{key}[/bold red]: {val}\n"
            return result
        else:
            return f"Temperature: {temperature}\nFeels Like: {feels_like_temperature}"

    def get_multiple_weathers(self, month: bool, date: str) -> Table | str:
        url = f"https://weather.com/weather/monthly/l/{self.location}"
        tree = self.get_content(url)

        dates = self.extract_content(
            tree, "span.CalendarDateCell--date--JO3Db", multiple=True
        )
        temperatures = self.extract_content(
            tree, "div.CalendarDateCell--temps--16oU1", multiple=True
        )
        temperatures = [
            temperature[: temperature.index("°")]
            + "/"
            + temperature[temperature.index("°") :]
            for temperature in temperatures
        ]

        # format dates and temperatures into dictionary for printing
        montly_data = {}
        for weekly_data in zip(dates, temperatures):
            montly_data[weekly_data[0]] = weekly_data[1]

        # print the whole month's temperatures
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

        # print temperatures of date range
        final_data = ""
        date_range = list(map(int, date.split("-")))

        for key, val in montly_data.items():
            if int(key) >= date_range[0] and int(key) <= date_range[1]:
                final_data += (
                    f"[bold green]{key}[/bold green]: {val}\n                 "
                )
        return final_data

    def get_extra_data(self, tree: lxml.html.HtmlElement) -> dict:
        """get extra data if verbose flag is used

        Returns:
            dict: dictionary containg the extra data
        """
        extra_data = {}
        extra_data_names = self.extract_content(
            tree,
            "div.WeatherDetailsListItem--label--2ZacS",
            multiple=True,
        )
        extra_data_values = self.extract_content(
            tree,
            "div.WeatherDetailsListItem--wxData--kK35q",
            multiple=True,
        )

        for data in zip(extra_data_names, extra_data_values):
            if data[0] == "Wind":
                wanted_value = (
                    data[1].replace("\xa0", " ").replace("Wind Direction", "")
                )
                extra_data[data[0]] = wanted_value
                continue
            if data[0] == "Pressure":
                extra_data[data[0]] = data[1].replace("Arrow Down", "")
                continue
            extra_data[data[0]] = data[1]

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
            loc = requests.get("http://ipinfo.io/json").json()["loc"]
            return loc
        geolocator = Nominatim(user_agent="MyApp")
        loc = geolocator.geocode(location)
        return f"{loc.latitude},{loc.longitude}"
