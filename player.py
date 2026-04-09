class Player:
    def __init__(self, name, partner=None, pos=None, skip=False, stuck=False):
        self.name = name
        self.pos = pos
        self.partner = partner
        self.skip = skip
        self.stuck = stuck

    def move(self, new_pos):
        self.pos = new_pos

        return print(f"Player {self.name} moved to {new_pos}")

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
