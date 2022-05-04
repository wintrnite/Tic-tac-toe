import typer
from pathlib import Path
from game_logic import start_game_commands


def main(
    n: int = typer.Argument(..., min=1, max=26),
    k: int = typer.Argument(..., min=1, max=26),
):
    """
    Enter the field size to start the game\n
    1 <= n <= 26, 1 <= k <= 26
    """
    typer.secho("Tic-tac-toe", fg=typer.colors.BRIGHT_CYAN)
    typer.secho(f"С заданными размерами поля надо собрать {min(n, k, 5)} в ряд для победы")
    if Path("saved.pickle").is_file():
        typer.echo('Найдена сохраненная игра, введите "l", чтоб продолжить её')
    command = typer.prompt(
        f'Введите "n", чтоб начать новую игру с размером поля {n} на {k}\n'
    )
    while command not in start_game_commands:
        typer.echo("Incorrect command")
        command = typer.prompt(
            f'Введите "n", чтоб начать новую игру с размером поля {n} на {k}\n'
        )
    program_state = start_game_commands[command](n, k)
    print(program_state)


if __name__ == "__main__":
    typer.run(main)
