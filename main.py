import typer
from typing_extensions import Annotated
from weather import Weather
from rich.console import Console
from urllib import request


app = typer.Typer()
console = Console()

    
def internet_on():
    try:
        request.urlopen("https://www.google.com", timeout=1)
        return True
    except request.URLError as err:
        return False

@app.command()
def main(
    date: Annotated[str, typer.Option("--date", "-d", help="Date range of the weather.", rich_help_panel="Options")] = "today",
    location: Annotated[str, typer.Option("--location", "-l", help="The desired locaiton of the weather. Deafults to user's ip location if not provided.", rich_help_panel="Options")] = "",
    unit: Annotated[str, typer.Option("--unit", "-u", help="Unit of the weather (celcius/farenheit).", rich_help_panel="Options")] = "c",
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Get more information (High / Low, Wind, Humidity, Dew Point, Pressure, UV Index, Visibility, Moon Phase).", rich_help_panel="Options")] = False,
):
    """
    Get weather of the desired location, date range, and units.
    
    Defaults to today's weather in user location in celcius. 
    """
    if not internet_on():
        console.print(":warning: [bold red]No interent connection. Aborting.[/bold red]")
        return
    weather = Weather(location=location, unit=unit)
    data = weather.get_weather(date=date, verbose=verbose)
    console.print(data)


if __name__ == "__main__":
    app()
