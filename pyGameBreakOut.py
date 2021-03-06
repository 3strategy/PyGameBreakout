  # game class (main)
try:
    import sys
    import re
    from player import *
    from ball import *
except ImportError as err:
    print("couldn't load module. %s" % err)
    sys.exit(2)


def main():
    # Initialise screen
    # pygame.init()
    # screen = pygame.display.set_mode((screenx, screeny),pygame.FULLSCREEN)
    screen = pygame.display.set_mode((screenx, screeny))

    pygame.display.set_caption('Blobby')

    background = pygame.image.load('data\\BlobbyBack.jpg')
    background = pygame.transform.scale(background, (screenx, screeny))
    background = background.convert()

    # Initialise players, net, and ball
    players = [Player("left")]
    net_1 = Brick(-500, 200)
    net = Brick(-350, 200)
    net1 = Brick(-200, 200)
    net2 = Brick(-50, 200)
    net3 = Brick(100, 200)
    net4 = Brick(250, 200)
    net5 = Brick(400, 200)
    net5b = Brick(550, 200)
    net6a = Brick(-500, 250)
    net6 = Brick(-350, 250)
    net7 = Brick(-200, 250)
    net8 = Brick(-50, 250)
    net9 = Brick(100, 250)
    net10 = Brick(250, 250)
    net11= Brick(400, 250)
    net12 = Brick(550, 250)
    boundry = Boundry()
    pointer = Pointer()
    bricksprites = pygame.sprite.RenderPlain(net_1,net, net1, net2, net3, net4, net5,net5b,net6a, net6, net7, net8, net9, net10, net11,net12)
    #bricksprites.remove(net1)

    ball = Ball(players, bricksprites, pointer, boundry)
    Player.ball = ball  # give player a static reference to ball.

    # Initialise sprites' groups
    playersprites = pygame.sprite.RenderPlain(players,boundry)
    ballsprites = pygame.sprite.RenderPlain(ball, pointer)


    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("Hello There", 1, (250, 250, 250))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx

    # Initialise clock
    clock = pygame.time.Clock()

    # Game loop
    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(54)

        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            # OOP:Don't ask for the information you need to do the work;
            # ask for the object that has information to do the work for you. (Allen Hollub)
            for player in players:
                player.move(event)

        p0 = players[0]
        info = f'{p0.life} '
        if p0.fault != Fault.Ok:
            fl = re.search(r'((\w*)\.(\w*))', f'{p0.fault}').group(3)
            info = f'{fl} {info}'
        #elif p1.fault != Fault.Ok:
        #    fl = re.search(r'((\w*)\.(\w*))', str(p1.fault)).group(3)
        #    info = f'{info}  {fl}'
        # info = f'{p0.state} {info}  {p1.state} dX:{p1.dX:.1f} dY:{p1.dY:.1f}'
        # info = f'{info} Ball dX:{ball.dX:.1f} dY:{ball.dY:.1f}'
        # note the : after which comes the formatting (here .1f for 1 decimal point)
        text = font.render(info, 1, (250, 250, 250))

        screen.blit(background, (0, 0))  # this acts as a clear screen (try without and see how everything smears)
        screen.blit(text, textpos)  # if we blit to background we are smearing.

        bricksprites.update()
        playersprites.update()  # it matters if you update the player before or after the ball.
        ballsprites.update()  # calls the update method on sprite

        bricksprites.draw(screen)
        playersprites.draw(screen)
        ballsprites.draw(screen)  # blits every sprite to the screen.

        pygame.display.flip()  # refreshses the display with the content of 'screen'


if __name__ == '__main__':
    main()
