import rps
import pytest


@pytest.fixture
def game():
    mg = rps.MainGame()

    return mg


@pytest.fixture
def check():
    return rps.check_handle


@pytest.fixture
def handle():
    return rps.handle_command


def test_users_0(game):
    game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")
    assert game.players == {"<@MARK>": 0, "<@FELIPE>": 0, "<@SHAWN>": 0}


def test_false_start(game):
    game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")
    assert not game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")


def test_users_1(game):
    game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")
    handle = "<@MARK>"
    selection = "rock"
    game.add(handle, selection)
    assert game.players == {"<@MARK>": 1, "<@FELIPE>": 0, "<@SHAWN>": 0}


def test_add_rock(game):
    game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")
    handle = "<@MARK>"
    selection = "rock"
    assert game.add(handle, selection)


def test_add_paper(game):
    game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")
    handle = "<@MARK>"
    selection = "paper"
    assert game.add(handle, selection)


def test_add_scissors(game):
    game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")
    handle = "<@MARK>"
    selection = "scissors"
    assert game.add(handle, selection)


def test_add_gibberish(game):
    game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")
    handle = "<@MARK>"
    selection = "papers"
    assert game.add(handle, selection) == 3


def test_add_non_user(game):
    game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")
    handle = "<@MARKs>"
    selection = "paper"
    assert game.add(handle, selection) == 2


def test_rock_paper(game):
    game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")
    game.add("<@MARK>", "rock")
    game.add("<@FELIPE>", "paper")
    assert game.play() == ["<@FELIPE>"]


def test_rock_scissors(game):
    game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")
    game.add("<@MARK>", "rock")
    game.add("<@FELIPE>", "scissors")
    assert game.play() == ["<@MARK>"]


def test_paper_scissors(game):
    game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")
    game.add("<@MARK>", "paper")
    game.add("<@FELIPE>", "scissors")
    assert game.play() == ["<@FELIPE>"]


def test_all_selections(game):
    game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")
    game.add("<@MARK>", "rock")
    game.add("<@FELIPE>", "paper")
    game.add("<@SHAWN>", "scissors")
    assert game.play() == []


def test_list_clears(game):
    game.new_game("<@MARK>", ["<@FELIPE>", "<@SHAWN>"], "CHANNEL")
    game.add("<@MARK>", "rock")
    game.add("<@FELIPE>", "paper")
    game.add("<@SHAWN>", "scissors")
    game.play()
    assert not len(game.d)


def test_handle_true(check):
    assert check("<@ajoiwefh2345rfSAT>")


def test_handle_false(check):
    assert not check("<@ajoiwefh2345rf%SAT>")


def test_handle_command_start_game(handle, game):
    assert handle(game, "challenge <@USLACKBOT>", "<@UTEST>",
                  "CHANNEL")[1] == \
        "Game Started with users <@USLACKBOT>"


def test_handle_command_non_user(handle, game):
    assert handle(game, "challenge <@USLA-CKBOT>", "<@UTEST>",
                  "CHANNEL")[1] == "I'm sorry, one of the users " \
        "you selected: '<@USLA-CKBOT>' is not properly formatted.  " \
        "Please try again using their @user Slack handle."


def test_handle_command_choose_valid(handle, game):
    handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    _, response = handle(game, "choose rock", "<@UTEST>", "CHANNEL")
    assert response == "Choice was successfully added"


def test_handle_command_choose_invalid_choice(handle, game):
    handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    _, response = handle(game, "choose rocks", "<@UTEST>", "CHANNEL")
    assert response == "Choice was not successfully added, " \
                       "the input 'rocks' is invalid."


def test_handle_command_choose_invalid_name(handle, game):
    handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    _, response = handle(game, "choose rocks", "<@UTDEST>", "CHANNEL")
    assert response == "Choice was not successfully added, " \
                       "it appears you're not in the current game, " \
                       "<@UTDEST>."


def test_handle_command_end_game(handle, game):
    handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    handle(game, "choose rock", "<@UTEST>", "CHANNEL")
    _, response = handle(game, "quit", "<@UTEST>", "CHANNEL")
    assert response == "Game ended."


def test_handle_command_false_start(handle, game):
    handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    handle(game, "choose rock", "<@UTEST>", "CHANNEL")
    _, response = handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    assert response == "A game with <@UTEST> <@USLACKBOT> is " \
        "already in progress.  Please contact them to end the game " \
        "or use the '@rps quit' command if you're not afraid to burn " \
        "it all to the ground."


def test_handle_invalid_command(handle, game):
    assert handle(game, "ksdjf <@USLACKBOT>", "<@UTEST>", "CHANNEL")[1] == \
        rps.DEFAULT_RESPONSE


def test_complete_game_one_rock(handle, game):
    handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    handle(game, "choose scissors", "<@USLACKBOT>", "CHANNEL")
    _, response = handle(game, "choose rock", "<@UTEST>", "CHANNEL")
    assert response == "<@UTEST> are a force to be reckoned with!" \
        "\nResults: \nRock - <@UTEST>\n" \
        "Paper - \nScissors - <@USLACKBOT>"


def test_complete_game_one_paper(handle, game):
    handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    handle(game, "choose rock", "<@USLACKBOT>", "CHANNEL")
    _, response = handle(game, "choose paper", "<@UTEST>", "CHANNEL")
    assert response == "<@UTEST> are a force to be reckoned with!" \
        "\nResults: \nRock - <@USLACKBOT>\n" \
        "Paper - <@UTEST>\nScissors - "


def test_complete_game_one_scissors(handle, game):
    handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    handle(game, "choose scissors", "<@USLACKBOT>", "CHANNEL")
    _, response = handle(game, "choose paper", "<@UTEST>", "CHANNEL")
    assert response == "<@USLACKBOT> are a force to be reckoned " \
        "with!\nResults: \nRock - \n" \
        "Paper - <@UTEST>\nScissors - <@USLACKBOT>"


def test_complete_game_multiple_rock(handle, game):
    handle(game, "challenge <@USLACKBOT> <@UOTHER>", "<@UTEST>", "CHANNEL")
    handle(game, "choose rock", "<@USLACKBOT>", "CHANNEL")
    handle(game, "choose rock", "<@UOTHER>", "CHANNEL")
    _, response = handle(game, "choose scissors", "<@UTEST>", "CHANNEL")
    assert response == "<@USLACKBOT> <@UOTHER> are a force to be " \
        "reckoned with!\nResults: \nRock - <@USLACKBOT> <@UOTHER>" \
        "\nPaper - \nScissors - <@UTEST>"


def test_complete_game_multiple_paper(handle, game):
    handle(game, "challenge <@USLACKBOT> <@UOTHER>", "<@UTEST>", "CHANNEL")
    handle(game, "choose rock", "<@USLACKBOT>", "CHANNEL")
    handle(game, "choose rock", "<@UOTHER>", "CHANNEL")
    _, response = handle(game, "choose paper", "<@UTEST>", "CHANNEL")
    assert response == "<@UTEST> are a force to be reckoned with!" \
        "\nResults: \nRock - <@USLACKBOT> <@UOTHER>" \
        "\nPaper - <@UTEST>\nScissors - "


def test_complete_game_multiple_scissors(handle, game):
    handle(game, "challenge <@USLACKBOT> <@UOTHER>", "<@UTEST>", "CHANNEL")
    handle(game, "choose scissors", "<@USLACKBOT>", "CHANNEL")
    handle(game, "choose scissors", "<@UOTHER>", "CHANNEL")
    _, response = handle(game, "choose paper", "<@UTEST>", "CHANNEL")
    assert response == "<@USLACKBOT> <@UOTHER> are a force to be " \
        "reckoned with!\nResults: \nRock - " \
        "\nPaper - <@UTEST>\nScissors - <@USLACKBOT> <@UOTHER>"


def test_complete_game_all_rocks(handle, game):
    handle(game, "challenge <@USLACKBOT> <@UOTHER>", "<@UTEST>", "CHANNEL")
    handle(game, "choose rock", "<@USLACKBOT>", "CHANNEL")
    handle(game, "choose rock", "<@UOTHER>", "CHANNEL")
    _, response = handle(game, "choose rock", "<@UTEST>", "CHANNEL")
    assert response == "It's a draw!\nResults: \nRock - " \
        "<@USLACKBOT> <@UOTHER> <@UTEST>\nPaper - \nScissors - "


def test_complete_game_all_papers(handle, game):
    handle(game, "challenge <@USLACKBOT> <@UOTHER>", "<@UTEST>", "CHANNEL")
    handle(game, "choose paper", "<@USLACKBOT>", "CHANNEL")
    handle(game, "choose paper", "<@UOTHER>", "CHANNEL")
    _, response = handle(game, "choose paper", "<@UTEST>", "CHANNEL")
    assert response == "It's a draw!\nResults: \nRock - " \
        "\nPaper - <@USLACKBOT> <@UOTHER> <@UTEST>\nScissors - "


def test_complete_game_all_scissors(handle, game):
    handle(game, "challenge <@USLACKBOT> <@UOTHER>", "<@UTEST>", "CHANNEL")
    handle(game, "choose scissors", "<@USLACKBOT>", "CHANNEL")
    handle(game, "choose scissors", "<@UOTHER>", "CHANNEL")
    _, response = handle(game, "choose scissors", "<@UTEST>", "CHANNEL")
    assert response == "It's a draw!\nResults: \nRock - " \
        "\nPaper - \nScissors - <@USLACKBOT> <@UOTHER> <@UTEST>"


def test_complete_game_all_options(handle, game):
    handle(game, "challenge <@USLACKBOT> <@UOTHER>", "<@UTEST>", "CHANNEL")
    handle(game, "choose rock", "<@USLACKBOT>", "CHANNEL")
    handle(game, "choose paper", "<@UOTHER>", "CHANNEL")
    _, response = handle(game, "choose scissors", "<@UTEST>", "CHANNEL")
    assert response == "It's a draw!\nResults: \nRock - " \
        "<@USLACKBOT>\nPaper - <@UOTHER>\nScissors - <@UTEST>"


def test_start_over(handle, game):
    handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    handle(game, "choose rock", "<@USLACKBOT>", "CHANNEL")
    handle(game, "quit", "<@UTEST>", "CHANNEL")
    handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    handle(game, "choose scissors", "<@USLACKBOT>", "CHANNEL")
    _, response = handle(game, "choose rock", "<@UTEST>", "CHANNEL")
    assert response == "<@UTEST> are a force to be reckoned with!" \
                       "\nResults: \nRock - <@UTEST>\n" \
        "Paper - \nScissors - <@USLACKBOT>"


def test_play_again(handle, game):
    handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    handle(game, "choose paper", "<@USLACKBOT>", "CHANNEL")
    handle(game, "choose rock", "<@UTEST>", "CHANNEL")
    handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    handle(game, "choose scissors", "<@USLACKBOT>", "CHANNEL")
    _, response = handle(game, "choose rock", "<@UTEST>", "CHANNEL")
    assert response == "<@UTEST> are a force to be reckoned with!\n" \
        "Results: \nRock - <@UTEST>\n" \
        "Paper - \nScissors - <@USLACKBOT>"


def test_add_no_users(handle, game):
    _, response = handle(game, "challenge", "<@UTEST>", "CHANNEL")
    assert response == rps.DEFAULT_RESPONSE


def test_status_game_in_progress_waiting(handle, game):
    handle(game, "challenge <@USLACKBOT>", "<@UTEST>", "CHANNEL")
    handle(game, "choose paper", "<@USLACKBOT>", "CHANNEL")
    _, response = handle(game, "status", "<@UTEST>", "CHANNEL")
    assert response == "There is currently a game in progress, " \
        "waiting for : <@UTEST> "


def test_status_no_game_in_progress_complete(handle, game):
    _, response = handle(game, "status", "<@UTEST>", "CHANNEL")
    assert response == "There is currently no game in progress."


def test_help_request(handle, game):
    _, response = handle(game, "help", "<@UTEST>", "CHANNEL")
    assert response == rps.HELP_TEXT
