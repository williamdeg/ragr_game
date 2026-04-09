from player import Player
import random
from gameplay import diceroll, occupied, rpc


def main():

    turncount = [0] * 99

    for i in range(0, 99):

        special_numbers = [2, 3, 7, 12]

        players = [
            Player("Karro"),
            Player("Erik"),
            Player("Micke"),
            Player("Pott"),
            Player("Wille"),
            Player("Jacob"),
        ]

        winner = False
        turncount[i] = 0
        space7 = []

        while not winner:

            for plr in players:
                if plr.skip:
                    print(f"{plr.getname()} skips this turn!")
                    plr.skip = False
                else:

                    dr = diceroll()
                    dr_sum = sum(dr)

                    if plr.stuck and (dr[0] != dr[1]):
                        print(
                            f"Player {plr.getname()} rolled a {dr_sum} ({dr[0]} + {dr[1]}). They need a pair to escape the dragon, and will skip this turn!"
                        )
                    else:

                        print(
                            f"Player {plr.getname()} rolled a {dr_sum} ({dr[0]} + {dr[1]})"
                        )

                        if plr.stuck:
                            print(f"They escaped the dragon!")
                            plr.stuck = False

                        plr.move(dr_sum)
                        ocpd = occupied(plr, players)

                        if dr_sum == 12 and plr.partner is not None:
                            print(
                                f"{plr.getname()} and {plr.partner.getname()} got married, and lived happily ever after. You win!"
                            )

                            winner = True
                            break
                        elif dr_sum == 2:
                            print(
                                f"{plr.getname()} got caught by the dragon! They need to roll a pair to escape!"
                            )
                            plr.stuck = True
                        elif dr_sum == 3:
                            plr.divorce
                        elif dr_sum == 7:
                            space7 = [
                                player for player in space7 if player.getpos() == 7
                            ]
                            if plr in space7:
                                space7.remove(plr)
                            space7.append(plr)

                            if len(space7) == 2:
                                space7[0].engage(space7[1])

                            elif len(space7) == 3:
                                print(
                                    f"Three players on 7! {space7[0].getname()} gets kicked off the board and divorces {space7[1].getname()}, who then gets engaged to {space7[2].getname()}! Drama!"
                                )

                                space7[0].divorce()
                                space7[0].pos = None
                                space7[0].skip = True
                                space7[1].engage(space7[2])
                                space7 = [space7[1], space7[2]]

                        if ocpd != None and dr_sum not in special_numbers:
                            print(
                                f"Space {dr_sum} is occupied by {ocpd[0].getname()}. This calls for rock, paper, scissors"
                            )

                            rpc_strings = ["rock", "paper", "scissors"]

                            rpc_res = rpc(
                                plr,
                                rpc_strings[random.randrange(3)],
                                ocpd[0],
                                rpc_strings[random.randrange(3)],
                            )

                            while rpc_res == None:
                                print("Tie, let's go again!")

                                rpc_res = rpc(
                                    plr,
                                    rpc_strings[random.randrange(3)],
                                    ocpd[0],
                                    rpc_strings[random.randrange(3)],
                                )

                            rpc_res[1].skip = True

                            print(
                                f"{rpc_res[0].getname()} wins! {rpc_res[1].getname()} is moved off the board, skips a turn, and has to drink!"
                            )

            turncount[i] = turncount[i] + 1
        print(f"Number of turns: {turncount[i]}")
    print(sum(turncount) / len(turncount))
    print(max(turncount))
    print(min(turncount))


if __name__ == "__main__":
    main()
