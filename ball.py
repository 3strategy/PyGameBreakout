# class Ball
try:
    from player import *
except ImportError as err:
    print("couldn't load module. %s" % err)
    sys.exit(2)


class Ball(SharedSprite):
    """A ball that will move across the screen"""

    def __init__(self, players, bricksprites, pointer, boundry):
        SharedSprite.__init__(self, 'VolleyGreenBig.png', 0.25)  # if using unusual size - use the scale to make it ok.
        self.hit = 0
        self.players: tuple[
            Player] = players  # type hinting is important. it helps seeing available methods in the class
        self.lastPlayer = False
        self.point_started = False
        self.point_scored = False
        self.bricksprites = bricksprites  # hinting.
        self.boundry: Boundry = boundry
        self.pointer: Pointer = pointer
        self.startY = 320 * basescale

        self.reinit()

    # call this each time a new point begins, to reset parameters and position.
    def reinit(self):
        self.point_started = False
        self.point_scored = False
        if self.lastPlayer:
            self.rect.center = (self.initial_wall_dist, self.startY)
        else:
            self.rect.center = (self.area.midright[0] - self.initial_wall_dist, self.startY)

        for player in self.players:
            player.reinit()

        SharedSprite.reinit(self)

        self.dY = 8
        self.dX = -8

    def score(self, fault):
        p: Player = self.players[0]
        p.life-=1
        if p.life==0: #stop the game
            p.fault = Fault.GameOver
            pygame.time.delay(3000)
            p.life = 4
            p.reinit()
        return
        # ordinal = self.area.centerx > self.rect.centerx
        # if not self.point_scored:  # prevent double scoring
        #     if fault is Fault.Net and self.players[not ordinal].num_shots == 0:
        #         return  # ignore net fault if player has not touched the ball yet.
        #     self.players[not ordinal].fault = fault
        #     if ordinal == self.lastPlayer:  # ball holder lost the point - switch ball.
        #         self.lastPlayer = not self.lastPlayer
        #     else:
        #         p: Player = self.players[ordinal]
        #         p.score += 1
        #         if p.score > 14 and p.score - self.players[not ordinal].score > 1:
        #             p.fault = Fault.Won
        #     self.point_scored = True

    def update(self, *args):
        SharedSprite.update(self)
        newpos, area = self.newpos, self.area
        self.pointer.rect.centerx = newpos.centerx
        # you can do the above pointing but you cannot do:
        # dY,dX = self.dY, self.dX  # WHY?
        # if self.point_started and self.dY < 14 * basescale:
        #     self.dY += self.gravity

        # All boundry tests run via Impulse Equations.
        if bestoverlap := self.bestoverlap(self.boundry):
            # everything (___, 51 or 52, or 53) means the ball hit the boundry floor
            if bestoverlap[1]>50: #?????????????? ????????
                #start new point (?????????? ???????? ??SCORE
                self.score(Fault.Floor)
                self.reinit()
                return
            self.process_impact(self.boundry, bestoverlap)
            if bestoverlap[1] > 75 * basescale:  # means ball touched the floor
                self.rollback()
                self.dY *= 0.7
                self.score(Fault.Floor)
                if -2 * basescale < self.dY < 2 * basescale:
                    self.reinit()
                    return

        # Brick collision detection ?????????? ?????????????? ????????
        for brick in self.bricksprites:
            if bestoverlap := self.bestoverlap(brick):  # testoverlap(self.net, self):
                self.bricksprites.remove(brick)
                temp_dx = self.dX
                self.process_impact(self.boundry, bestoverlap)
                if self.dX * temp_dx < 0:  # means ball bounced back
                    self.score(Fault.Net)

        # Player Collision testing ?????????? ?????????? ???????? ??????????
        for ordinal in range(1):
            player = self.players[ordinal]
            # overlap gets the result of the collision test and then an 'if' checks overlap
            if bestoverlap := self.bestoverlap(player):
                self.process_impact(player, bestoverlap)

                # reset num_shots of the THE OTHER PLAYER
                #self.players[not ordinal].num_shots = 0
                if not self.point_scored:
                    player.num_shots += 1
                if player.num_shots > 3:
                    self.score(Fault.Touch3)
                    return

                self.point_started = True  # from here on gravity will apply.
                return  # no need to check the other player.
