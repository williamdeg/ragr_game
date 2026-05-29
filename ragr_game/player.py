from PIL import Image, ImageDraw, ImageOps
from paths import BASE, ASSETS, PICS, FONTS
from board_spaces import BOARD_POSITIONS
import os
import random
import pygame


class Player:
    def __init__(
        self,
        name,
        marker=None,
        partner=None,
        pos=1,
        skip=False,
        stuck=False,
    ):
        self.name = name
        self.marker = marker
        self.pos = pos
        self.xy_pos = BOARD_POSITIONS[pos]
        self.oldpos = pos
        self.partner = partner
        self.skip = skip
        self.stuck = stuck

    def create_marker(self):

        # spec_names = ["karro", "erik", "micke", "pott", "jacob", "wille"]
        spec_names = ["karro", "wille"]

        if self.name.lower() in spec_names:
            player_pic = Image.open(
                PICS / "plr_pics" / f"{self.name.lower()}.jpg"
            ).convert("RGBA")
        else:
            rand = random.randint(1, 2)
            player_pic = Image.open(
                PICS / "plr_pics" / f"marker_misc_{str(rand)}.png"
            ).convert("RGBA")

        frame = Image.open(PICS / "plr_pics" / f"marker.png").convert("RGBA")

        frame_width = frame.width
        frame_height = frame.height
        padding = 2

        player_pic = ImageOps.fit(
            player_pic,
            (frame_width, frame_height),
            Image.Resampling.LANCZOS,
        )

        mask = Image.new("L", (frame_width, frame_height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse(
            (
                padding,
                padding,
                frame_width - padding,
                frame_height - padding,
            ),
            fill=255,
        )

        marker = Image.new("RGBA", (player_pic.width, player_pic.height), (0, 0, 0, 0))
        marker.paste(player_pic, mask=mask)
        marker.paste(frame, mask=frame)

        save_string = PICS / "plr_pics" / f"{self.name}_marker.png"
        marker.save(save_string, "PNG")
        self.marker = pygame.image.load(save_string)
        os.remove(PICS / "plr_pics" / f"{self.name}_marker.png")

    def move(self, tar_pos):
        self.pos = tar_pos

        # return print(f"Player {self.name} moved to {tar_pos}")

    def engage(self, player):
        if self.partner is None and player.partner is None:
            self.partner = player
            player.partner = self
            print(f"{self.getname()} got engaged to {player.getname()}!")
        elif self.partner is not None and player.partner is None:
            div_partner = self.getpartner()
            self.divorce()
            self.partner = player
            player.partner = self

            print(
                f"{self.getname()} broke off their engagement to {div_partner.getname()} and got engaged to {player.getname()}!"
            )
        elif self.partner is None and player.partner is not None:
            div_partner = player.getpartner()
            div_partner.divorce()
            player.divorce()
            print(
                f"{self.getname()} got engaged to {player.getname()}, who broke off their engagement to {div_partner.getname()}!"
            )
        elif self.partner is not None and player.partner is not None:
            div_partner1 = self.getpartner()
            div_partner2 = player.getpartner()

            self.divorce()
            player.divorce()
            self.partner = player
            player.partner = self

            print(
                f"{self.getname()} broke off their engagement to {div_partner1.getname()}, and got engaged to {player.getname()}, who broke off their engagement to {div_partner2.getname()}!"
            )

    def divorce(self):
        if self.partner is not None:
            div_partner = self.partner
            self.partner = None
            div_partner.partner = None

    def skip(self):
        if not self.skip:
            self.skip = True

    def stuck(self):
        if not self.stuck:
            self.stuck = True

    def getname(self):
        return self.name

    def getpos(self):
        return self.pos

    def getpartner(self):
        return self.partner
