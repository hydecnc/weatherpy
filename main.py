import typer
from typing_extensions import Annotated, Optional

# from rich import print
from weather import get_weather


app = typer.Typer()


@app.command()
def main(
    verbosity: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Get more information (High / Low, Wind, Humidity, Dew Point, Pressure, UV Index, Visibility, Moon Phase)",
    ),
    date: str = typer.Option(
        "today",
        "--date"
        "-d"
    ),
    location: str = "",
    unit: str = "c",
):
    print(f"{get_weather(date, location, unit, verbosity)}")


if __name__ == "__main__":
    app()
