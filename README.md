Welcome to Rock Paper Scissors on Slack!
========================================

>'Rock-paper-scissors (also known as paper, rock, scissors
or paper, scissors, stone) is a hand game usually played
between two people, in which each player simultaneously
forms one of three shapes with an outstretched hand. These
shapes are "rock" (a simple fist), "paper" (a flat hand),
and "scissors" (a fist with the index and middle fingers
extended, forming a V). A zero-sum game, it has only two
possible outcomes other than a tie: one of the two players
wins, and the other player loses.'

_Wikipedia, 2017_

The Rock Paper Scissors Slack bot allows for real-time
gameplay across geographically dislocated teams.  There
is no limit to the number of players allowed, and there
is no limite to the amount of fun to be had!

_Commands:_
-----------------

Challenge:
----------
Starts a new game, challenging other Slack
users by their handles, separated by spaces.

__Usage:__
- `@rps challenge @user @user...`

Choose:
------
Respond to a challenge by selecting your weapon of choice 
(rock, paper or scissors). When the last player has chosen 
then the winner(s) will be announced.  You can use your 
private rps bot conversation to select your choice to maintain 
competitive secrecy! This command can also be entered multiple 
times per turn, although only the most recent entry will be 
used.

__Usage:__
- `@rps choose rock`
- `@rps choose paper`
OR
- `@rps choose scissors`

Help:
-----
Display this help message.

__Usage:__
- `@rps help`

Quit:
-----      
Quits any active game without prompting for
permission or notifying the players.  Since
this bot can only manage one game at a time
this will affect anyone and everyone.  Please
use wisely.

__Usage:__
- `@rps quit`

Status:
-------
Returns a message describing whether or not
there is a current game, and what players, if
any, have yet to complete their turn.

__Usage:__
- `@rps status`

_**This rps bot is brought to you by amne51ac.**_

_rpsls coming soon_