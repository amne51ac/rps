import collections
import time
import re
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = "U6Q9DDLJC"

# constants
AT_BOT = "<@" + BOT_ID + ">"
START_GAME = "challenge"
CHOOSE = "choose"
END_GAME = "quit"
STATUS = "status"
HELP = "help"

# instantiate Slack & Twilio clients
slack_client = SlackClient("xoxb-228319462624-KdHljs7h3NDysE0G0laCQ4xj")

ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"

DEFAULT_RESPONSE = """I did not recognize your message.
If you'd like to start a game, please send:
@rps challenge @user @user etc.

If you need more information you may use:
@rps help"""

HELP_TEXT = """Welcome to Rock Paper Scissors on Slack!

'Rock-paper-scissors (also known as paper, rock, scissors
or paper, scissors, stone) is a hand game usually played
between two people, in which each player simultaneously
forms one of three shapes with an outstretched hand. These
shapes are "rock" (a simple fist), "paper" (a flat hand),
and "scissors" (a fist with the index and middle fingers
extended, forming a V). A zero-sum game, it has only two
possible outcomes other than a tie: one of the two players
wins, and the other player loses.'

(Wikipedia, 2017)

The Rock Paper Scissors Slack bot allows for real-time
gameplay across geographically dislocated teams.  There
is no limit to the number of players allowed, and there
is no limite to the amount of fun to be had!

The commands are:

challenge - Starts a new game, challenging other Slack
            users by their handles, separated by spaces.

            Usage:
                @rps challenge @user @user...

choose -    Respond to a challenge by selecting your
            weapon of choice (rock, paper or scissors).
            When the last player has chosen then the
            winner(s) will be announced.  You can use
            your private rps bot conversation to select
            your choice to maintain competitive secrecy!
            This command can also be entered multiple times
            per turn, although only the most recent entry
            will be used.

            Usage:
                @rps choose rock
                @rps choose paper
                OR
                @rps choose scissors

help -      Display this help message.

            Usage:
                @rps help

quit -      Quits any active game without prompting for
            permission or notifying the players.  Since
            this bot can only manage one game at a time
            this will affect anyone and everyone.  Please
            use wisely.

            Usage:
                @rps quit

status -    Returns a message describing whether or not
            there is a current game, and what players, if
            any, have yet to complete their turn.

            Usage:
                @rps status

The rps bot is brought to you by Mark Milhouse

---rpsls coming soon---"""

HANDLE_PATTERN = re.compile("^\<\@[0-9a-zA-Z]{1,}\>$")


def check_handle(handle):
    if HANDLE_PATTERN.match(handle):
        return True
    else:
        return False


class MainGame:

    def __init__(self):
        self.d = collections.defaultdict(list)
        self.players = {}
        self.channel = ""

    def new_game(self, user, handles, channel):
        if len(self.players.values()):
            return 0
        self.players[user.upper()] = 0
        for i in handles:
            self.players[i.upper()] = 0
        self.channel = channel
        return 1

    def add(self, handle, selection):
        if handle.upper() in self.players:
            if selection.lower() in [ROCK, PAPER, SCISSORS]:
                self.players[handle.upper()] = 1
                self.d[selection].append(handle.upper())
                return 1
            else:
                return 3
        else:
            return 2

    def play(self):
        selects = self.d.keys()
        if ROCK in selects and PAPER in selects and SCISSORS in selects:
            self.clear()
            return []
        elif ROCK in selects and PAPER in selects:
            result = self.d[PAPER]
            self.clear()
            return result
        elif ROCK in selects and SCISSORS in selects:
            result = self.d[ROCK]
            self.clear()
            return result
        elif PAPER in selects and SCISSORS in selects:
            result = self.d[SCISSORS]
            self.clear()
            return result
        else:
            return []

    def clear(self):
        self.channel = ""
        self.players.clear()
        self.d.clear()


def handle_command(game, command, user, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    prefix = command.strip().split(" ")[0]
    suffix = command.strip().split(" ")[1:]

    if prefix == START_GAME:
        if len(suffix):
            for i in suffix:
                if not check_handle(i):
                    return None, "I'm sorry, one of the users you selected: " \
                        "'" + i + "' is not properly formatted.  Please " \
                        "try again using their @user Slack handle."
            if game.new_game(user, suffix, channel):
                return None, "Game Started with users " + \
                    " ".join(suffix).upper()

            else:
                return None, "A game with " + \
                    " ".join(game.players.keys()).upper() + " is already in " \
                    "progress.  Please contact them to end the game or use " \
                    "the '@rps quit' command if you're not afraid to burn " \
                    "it all to the ground."
        else:
            return None, DEFAULT_RESPONSE

    elif prefix == CHOOSE:
        code = game.add(user, suffix[0])
        if code == 1:
            if 0 in game.players.values():
                return None, "Choice was successfully added"

            else:
                players = game.d.copy()
                to_channel = game.channel
                winners = game.play()

                if len(winners):
                    return to_channel, " ".join(winners).upper() + \
                        " are a force to be reckoned with!\nResults: \n" \
                        "Rock - " + " ".join(players["rock"]).upper() + "\n" \
                        "Paper - " + " ".join(players["paper"]).upper() + \
                        "\nScissors - " + " ".join(players["scissors"]).upper()

                else:
                    return to_channel, "It's a draw!\nResults: \n" \
                        "Rock - " + " ".join(players["rock"]).upper() + "\n" \
                        "Paper - " + " ".join(players["paper"]).upper() + \
                        "\nScissors - " + " ".join(players["scissors"]).upper()

        elif code == 2:
            return None, "Choice was not successfully added, " \
                "it appears you're not in the current game, " \
                + user.upper() + "."

        elif code == 3:
            return None, "Choice was not successfully added, " \
                "the input '" + suffix[0] + "' is invalid."

    elif prefix == END_GAME:
        game.clear()
        return None, "Game ended."

    elif prefix == STATUS:
        if 0 in game.players.values():
            return None, "There is currently a game in progress, " \
                "waiting for : " + \
                " ".join(key if not value else ""
                         "" for key, value in game.players.items())
        elif game.players:
            return None, "There is currently a game in progress, but " \
                         "all players have played."
        else:
            return None, "There is currently no game in progress."

    elif prefix == HELP:
        return None, HELP_TEXT

    return None, DEFAULT_RESPONSE


def parse_output(slack_rtm_output):  # pragma: no cover
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                    output['channel'], output['user']
    return None, None, None


if __name__ == "__main__":  # pragma: no cover
    game = MainGame()
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel, user = parse_output(slack_client.rtm_read())
            if command and channel and user:
                user = "<@" + user + ">"
                channel_to, response = handle_command(game, command,
                                                      user.upper(), channel)
                print("channel:", channel_to)
                slack_client.api_call("chat.postMessage",
                                      channel=channel_to if channel_to
                                      else channel, text=response,
                                      as_user=True)
            elif channel and user:
                slack_client.api_call("chat.postMessage", channel=channel,
                                      text=DEFAULT_RESPONSE, as_user=True)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
