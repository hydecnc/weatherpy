import typer
from typing_extensions import Annotated
from typing import Optional
from weatherpy.weather import Weather
from rich.console import Console
from urllib import request


app = typer.Typer()
console = Console()


def internet_on() -> bool:
    try:
        request.urlopen("https://www.google.com", timeout=1)
        return True
    except request.URLError:
        return False


def valid_options(
    date: str, location: str, unit: str, month: bool, verbose: bool
) -> bool | None:
    if month and date != "today":
        console.print(
            "[bold red]invalid option, month cannot be used with date.[/bold red]"
        )
        return False
    if date != "today" and verbose:
        console.print(
            "[bold red]Verbose flag is only available for today's weather.[/bold red]"
        )
        return False

    return True


@app.command()
def main(
    location: Annotated[
        Optional[str],
        typer.Argument(
            help="The desired locaiton of the weather. Deafults to user's ip location if not provided.",
        ),
    ] = "",
    date: Annotated[
        str,
        typer.Option(
            "--date",
            "-d",
            help='Date range of the weather. DATES are in format of dd seperated by " - " to define a range of date. A single number as DATE will be recognized as the day of the current month and year. CANNOT be used with --month.',
            rich_help_panel="Options",
        ),
    ] = "today",
    unit: Annotated[
        str,
        typer.Option(
            "--unit",
            "-u",
            help="Unit of the weather (celcius/farenheit).",
            rich_help_panel="Options",
        ),
    ] = "c",
    month: Annotated[
        bool,
        typer.Option(
            "--month",
            "-m",
            help="Get high/low temperature of the current month in a calendar. CANNOT be used with --date.",
            rich_help_panel="Options",
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Get more information (High / Low, Wind, Humidity, Dew Point, Pressure, UV Index, Visibility, Moon Phase). Only available with --date=today's weather.",
            rich_help_panel="Options",
        ),
    ] = False,
):
    """
    Get weather of the desired location, date range, and units.

    Defaults to today's weather in user location in celcius.
    """
    if not valid_options(date, location, unit, month, verbose):
        return
    if not internet_on():
        console.print(
            ":warning: [bold red]No interent connection. Aborting.[/bold red]"
        )
        return
    weather = Weather(location=location, unit=unit)
    data = weather.get_weather(date=date, month=month, verbose=verbose)
    console.print(data)


if __name__ == "__main__":
    app()
