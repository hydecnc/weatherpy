import typer
from typing_extensions import Annotated
from weather import Weather


app = typer.Typer()


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
    weather = Weather(location=location, unit=unit)
    print(f"{weather.get_weather(date=date, verbose=verbose)}")


if __name__ == "__main__":
    app()
