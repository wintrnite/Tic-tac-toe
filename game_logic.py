import pickle
import typer
import string
from pathlib import Path
from game_field import GameField
from artificial_intelligence import ArtificialIntelligence


def start_new_game(y: int, x: int):
    correct_choices = {"x", "X", "0", "O", "o"}
    side_choice = typer.prompt(
        "Choose which side you will play\n"
        'Enter "X" for first move\n'
        'Enter "O" for second move\n'
    )
    while side_choice not in correct_choices:
        typer.echo("Cannot understand your choice")
        side_choice = typer.prompt(
            "Choose which side you will play\n"
            'Enter "X" for first move\n'
            'Enter "O" for second move\n'
        )
    field = GameField(y, x, side_choice)
    end_game_message = play_game(field)
    return end_game_message


def load_saved_game():
    if Path("saved.pickle").is_file():
        with open("saved.pickle", "rb") as handle:
            field = pickle.load(handle)
            play_game(field)
    return "Save is not found"


def save_game(field: GameField):
    with open("saved.pickle", "wb") as handle:
        pickle.dump(field, handle, protocol=pickle.HIGHEST_PROTOCOL)
    end_game(field, "This is your saved game, see you later")


def play_game(field: GameField):
    ai = ArtificialIntelligence()
    while not field.has_game_over():
        if not field.is_player_turn():
            ai_make_move(ai, field)
            continue
        typer.echo(field)
        player_input = typer.prompt(
            "Enter coordinates of your move\n"
            'or enter "s" to save the game\n'
            'or enter "q" to quit the game\n'
        )
        if player_input in playing_command:
            playing_command[player_input](field)
            break
        player_make_move(player_input, field)
    if field.has_draw:
        end_game(field, "FRIENDSHIP FINALLY WON")
    return field.end_game_message


def player_make_move(player_input, field):
    coordinates = player_input.split()
    if try_make_move(field, coordinates):
        if field.has_win():
            end_game(field, "YOU WIN")
        field.switch_turn()
    else:
        typer.echo("Incorrect move")


def ai_make_move(ai, field):
    ai.make_move(field)
    if field.has_win():
        end_game(field, "YOU LOSE")
    field.switch_turn()


def end_game(field: GameField, message: str):
    typer.echo(message)
    typer.echo(field)
    field.game_over()
    field.end_game_message = "Game is over\nStart program to play again :)"


def try_make_move(field: GameField, coordinates: list) -> bool:
    letters = string.ascii_letters
    if len(coordinates) == 2:
        x, y = 0, 0
        if coordinates[0].isdigit() and coordinates[1] in letters:
            x, y = int(coordinates[0]) - 1, letters.find(coordinates[1])
        elif coordinates[1].isdigit() and coordinates[0] in letters:
            x, y = int(coordinates[1]) - 1, letters.find(coordinates[0])
        if field.try_put(x, y):
            return True
    return False


start_game_commands = {
    "n": lambda n, k: start_new_game(n, k),
    "l": lambda n, k: load_saved_game(),
}

playing_command = {
    "s": lambda field: save_game(field),
    "q": lambda field: end_game(field, "You quit the game"),
}
