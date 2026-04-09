import random


def diceroll():
    dice1 = random.randrange(1, 7)
    dice2 = random.randrange(1, 7)

    return [dice1, dice2]


def occupied(this_player, players):

    player_list = []

    for player in players:
        if (player.getpos() == this_player.getpos()) and (
            player.getname() != this_player.getname()
        ):
            player_list.append(player)

    if player_list:
        return player_list
    else:
        return None


def rpc(player1, pick1, player2, pick2):

    match pick1:
        case "rock":
            if pick2 == "rock":
                return None
            elif pick2 == "paper":
                player1.pos = None
                return [player2, player1]
            elif pick2 == "scissors":
                player2.pos = None
                return [player1, player2]

        case "paper":
            if pick2 == "rock":
                player2.pos = None
                return [player1, player2]
            elif pick2 == "paper":
                return None
            elif pick2 == "scissors":
                player1.pos = None
                return [player2, player1]

        case "scissors":
            if pick2 == "rock":
                player1.pos = None
                return [player2, player1]
            elif pick2 == "paper":
                player2.pos = None
                return [player1, player2]
            elif pick2 == "scissors":
                return None
