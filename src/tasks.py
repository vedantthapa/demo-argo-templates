import typer

app = typer.Typer()


@app.command()
def say(message: str):
    print(message)


@app.command()
def fail_random():
    import random
    import sys

    exit_code = random.choice([0, 1, 1])
    sys.exit(exit_code)


if __name__ == "__main__":
    app()
