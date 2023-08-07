import typer
from rich import print
from weather import get_weather

app = typer.Typer()

@app.command()
def main(date: str = "today", location: str = "", unit: str = "c"):
    # print(f"Weather {date} is shiny")
    print(f"[bold red]{get_weather(date, location, unit)}[/bold red]")

if __name__ == "__main__":
    app()