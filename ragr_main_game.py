import sys, pygame
import os
import time
import random


from gameplay import diceroll, occupied, rps
from player import Player
from button import Button
from textbox import Textbox

from paths import BASE, ASSETS, PICS, FONTS
from board_spaces import BOARD_POSITIONS

pygame.init()

# Game state
state = "menu"

# Window settings
size = width, height = 1000, 1000
black = 0, 0, 0
screen = pygame.display.set_mode(size)

# -------------------MENU-------------------
# Menu visuals
menu_background = pygame.image.load(PICS / "wooden-texture.jpg")
menu_background = pygame.transform.scale(menu_background, (1000, 1000))
menu_overlay = pygame.image.load(PICS / "menu_overlay.png")
add_player_overlay = pygame.image.load(PICS / "add_player_overlay.png")
delete_player_x = pygame.image.load(PICS / "x_button.png")

# Menu items
play_button = Button((150, 412, 278, 138), "play")
close_add_player = Button((800, 160, 40, 40), "close_add_player")
add_player_button = Button((580, 412, 278, 138), "add_player")
add_player_textbox = Textbox(50, FONTS / "Norse-KaWl.otf", (250, 245, 500, 50))
player_list_textbox = Textbox(50, FONTS / "Norse-KaWl.otf", (100, 525, 500, 300))
delete_player_button = Button((860, 610, 50, 50), "delete_player")
# ------------------------------------------

# -------------------GAME-------------------
# Game visuals
game_background = pygame.image.load(PICS / "wooden-texture.jpg")
game_background = pygame.transform.scale(game_background, (1000, 1000))
board = pygame.image.load(PICS / "board_pattern.png")
roll_background = pygame.image.load(PICS / "roll_button.png")
player_turn_bar = pygame.image.load(PICS / "player_turn_bar.png")
ring_icon = pygame.image.load(PICS / "plr_pics" / "ring.png")
player_turn_text = Textbox(50, FONTS / "Norse-KaWl.otf", (400, 25, 200, 75))

# Game items
roll_button = Button((360, 885, 280, 90), "roll die")
die_imgs = {
    1: pygame.image.load(PICS / "die_one.png"),
    2: pygame.image.load(PICS / "die_two.png"),
    3: pygame.image.load(PICS / "die_three.png"),
    4: pygame.image.load(PICS / "die_four.png"),
    5: pygame.image.load(PICS / "die_five.png"),
    6: pygame.image.load(PICS / "die_six.png"),
}
# ------------------------------------------

# --------------------RPS--------------------
# RPS visuals
rps_screen = pygame.image.load(PICS / "rps_screen.png")

# RPS items
r_button = Button((620, 250, 250, 300), "rock")
p_button = Button((350, 250, 250, 300), "paper")
s_button = Button((150, 250, 200, 300), "scissors")
player_pick_textbox = Textbox(80, FONTS / "NorseBold-2Kge.otf", (375, 595, 200, 100))


# Game vars
players = list()
player_names = list()
plr = None
turncount = 0
dr = None
max_players = 6
player_pos_offset = 0
enter_name = False
animation = False
step = 10
winner = False
space7 = []
ocpd = None
offset = -50

goto_rps = False
rps_res = None
p1_pick = None
p2_pick = None
timer = None


# Functions
def interp(p1, p2, step):

    step_x = (p2[0] - p1[0]) / step
    step_y = (p2[1] - p1[1]) / step

    x = p1[0] + step_x
    y = p1[1] + step_y

    return x, y


# Main loop
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if state == "menu":

            if (
                (
                    play_button.pressed(event)
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)
                )
                and players
                and enter_name == False
            ):
                state = "game"

            if add_player_button.pressed(event):
                enter_name = True
                add_player_textbox.active = True
                add_player_textbox.clear_text()

            if close_add_player.pressed(event) and enter_name == True:
                enter_name = False

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_RETURN
                and enter_name == True
                and (
                    add_player_textbox.get_text() is None
                    or add_player_textbox.get_text() == ""
                )
            ):
                enter_name = False

            if enter_name:
                player_name = add_player_textbox.event_handler(event)

                if player_name and len(player_names) < max_players:
                    add_player_textbox.clear_text()
                    player = Player(player_name)
                    player.create_marker()

                    players.append(player)
                    player_tb = Textbox(
                        40,
                        FONTS / "Norse-KaWl.otf",
                        (100, 520 + player_pos_offset, 500, 300),
                    )
                    player_tb.set_text(
                        f"Player {len(player_names)+1}:           {player.name}"
                    )
                    player_names.append(player_tb)
                    player_pos_offset += 47

            if delete_player_button.pressed(event) and player_names:
                players.pop()
                player_names.pop()
                player_pos_offset -= 47

        elif state == "game":

            # turncount = [0] * 99

            # for i in range(0, 99):

            special_numbers = [2, 4, 7, 12]

            # players = [
            # Player("Karro"),
            # Player("Erik"),
            # Player("Micke"),
            #  Player("Pott"),
            #  Player("Wille"),
            #   Player("Jacob"),
            # ]

            if not winner and not animation:

                plr = players[turncount]

                if plr.skip:
                    print(f"{plr.getname()} skips this turn!")
                    plr.skip = False

                    if turncount == len(players) - 1:
                        turncount = 0
                    else:
                        turncount += 1
                else:
                    if roll_button.pressed(event) or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN
                    ):

                        dr = diceroll()
                        dr_sum = sum(dr)

                        if turncount == len(players) - 1:
                            turncount = 0
                        else:
                            turncount += 1

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

                            if (
                                occupied(plr, players) is not None
                                and dr_sum not in special_numbers
                            ):
                                ocpd = occupied(plr, players)
                                goto_rps = True

                            if dr_sum == 12 and plr.partner is not None:
                                print(
                                    f"{plr.getname()} and {plr.partner.getname()} got married, and lived happily ever after. You win!"
                                )

                                winner = True
                            elif dr_sum == 2:
                                print(
                                    f"{plr.getname()} got caught by the dragon! They need to roll a pair to escape!"
                                )
                                plr.stuck = True
                            elif dr_sum == 4 and plr.partner is not None:
                                spouse = plr.getpartner()
                                plr.divorce
                                spouse.move(dr_sum)
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

        elif state == "rps" and timer is None:
            if p1_pick is None:
                if r_button.pressed(event):
                    p1_pick = "rock"
                elif p_button.pressed(event):
                    p1_pick = "paper"
                elif s_button.pressed(event):
                    p1_pick = "scissors"
            elif p1_pick is not None and p2_pick is None:
                if r_button.pressed(event):
                    p2_pick = "rock"
                elif p_button.pressed(event):
                    p2_pick = "paper"
                elif s_button.pressed(event):
                    p2_pick = "scissors"

            if (
                p1_pick is not None
                and p2_pick is not None
                and ocpd is not None
                and rps_res is None
            ):
                rps_res = rps(ocpd, p1_pick, p2_pick)

                if rps_res == "tie":
                    rps_res = None
                else:
                    print(f"{rps_res[0].name} wins!")
                    rps_res[1].move(1)
                    ocpd = None

                p1_pick = None
                p2_pick = None

    if state == "menu":

        screen.blit(menu_background, (0, 0))
        screen.blit(menu_overlay, (0, 0))

        if player_names:

            screen.blit(delete_player_x, (860, 610))

            for tb in player_names:
                tb.draw(screen)

        if enter_name:
            screen.blit(add_player_overlay, (0, 0))
            add_player_textbox.draw(screen)

    elif state == "game":
        screen.blit(game_background, (0, 0))
        screen.blit(board, (75, 100))
        screen.blit(roll_background, (0, 50))

        if plr is not None:
            screen.blit(player_turn_bar, (0, -25))

            if turncount == len(players):
                player_turn_text.set_text(f"{players[0].name}'s turn")
            else:
                player_turn_text.set_text(f"{players[turncount].name}'s turn")

            player_turn_text.draw(screen)

            if dr is not None:
                screen.blit(die_imgs[dr[0]], (700, 875))
                screen.blit(die_imgs[dr[1]], (850, 875))

            for plr_idle in players:
                screen.blit(plr_idle.marker, plr_idle.xy_pos)

                if plr_idle.partner:
                    screen.blit(
                        ring_icon, [plr_idle.xy_pos[0] + 25, plr_idle.xy_pos[1] - 20]
                    )

                # if plr.pos:

                if ocpd and plr_idle.name == ocpd[1].name:

                    if (
                        abs(
                            plr_idle.xy_pos[0]
                            - BOARD_POSITIONS[plr_idle.pos][0]
                            + offset
                        )
                        < 5
                        and abs(plr_idle.xy_pos[1] - BOARD_POSITIONS[plr_idle.pos][1])
                        < 5
                    ):
                        plr_idle.xy_pos = [
                            BOARD_POSITIONS[plr_idle.pos][0] + offset,
                            BOARD_POSITIONS[plr_idle.pos][1],
                        ]
                        animation = False

                        if goto_rps:
                            state = "rps"
                            goto_rps = False
                    else:
                        animation = True
                        plr_idle.xy_pos = interp(
                            plr_idle.xy_pos,
                            [
                                BOARD_POSITIONS[plr_idle.pos][0] + offset,
                                BOARD_POSITIONS[plr_idle.pos][1],
                            ],
                            step,
                        )
                else:
                    if (
                        abs(plr.xy_pos[0] - BOARD_POSITIONS[plr.pos][0]) < 5
                        and abs(plr.xy_pos[1] - BOARD_POSITIONS[plr.pos][1]) < 5
                    ):
                        plr.xy_pos = [
                            BOARD_POSITIONS[plr.pos][0],
                            BOARD_POSITIONS[plr.pos][1],
                        ]
                        animation = False

                        if goto_rps:
                            state = "rps"
                            goto_rps = False
                    else:
                        animation = True
                        plr.xy_pos = interp(
                            plr.xy_pos,
                            [
                                BOARD_POSITIONS[plr.pos][0],
                                BOARD_POSITIONS[plr.pos][1],
                            ],
                            step,
                        )

    elif state == "rps" and not animation:
        screen.blit(game_background, (0, 0))
        screen.blit(board, (75, 50))
        screen.blit(rps_screen, (0, 0))

        if rps_res is not None and rps_res != "tie":
            player_pick_textbox.set_text(f"{rps_res[0].name} wins!!!")
            player_pick_textbox.draw(screen)

            if timer is None:
                timer = pygame.time.get_ticks()

            if (pygame.time.get_ticks() - timer) > 3000:
                timer = None
                rps_res = None
                player_pick_textbox.set_text("")
                state = "game"
        else:
            player_pick_textbox.draw(screen)

        if ocpd is not None:
            if p1_pick is None:
                player_pick_textbox.set_text(f"{ocpd[0].name}, make your pick!")
            elif p2_pick is None:
                player_pick_textbox.set_text(f"{ocpd[1].name}, make your pick!")

    pygame.display.flip()
