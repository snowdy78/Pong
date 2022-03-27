from config import *
import random


def get_clicked(before: bool, after: bool):
    return not before and after


def draw_points(screen, points):
    if points:
        for p in points:
            c = Circle(p, 5)
            c.color = Color(255, 50, 50)
            c.draw(screen)

def get_text_width(text: str, char_size: int):
    return floor(len(text) * char_size / 2.926829268292683)


def test1(screen: pg.Surface):
    res = screen.get_size()
    vres = Vector2(res)
    countofballs = 100
    balls = list()
    screen_rect = Rectangle(vres / 2, vres)
    for i in range(countofballs):
        spread = 180
        rand1 = random.randint(3 * spread, 5 * spread)
        rand2 = random.randint(-spread, spread)
        rand = rand1 if random.randint(0, 1) else rand2
        ball = Ball(Vector2(res[0] / 2, res[1] / 2), Vector2(cos(rand * pi / 180), sin(rand * pi / 180)), 5)
        balls.append(ball)
        del ball

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
        screen.fill((0, 0, 0))
        for ball in balls:
            ball.speed = 5
            ball.move([screen_rect])
            ball.draw(screen)
        pg.display.update()


def test2(screen: pg.Surface):
    res = screen.get_size()
    vres = Vector2(res)
    countofballs = 100
    balls = list()
    screen_rect = Rectangle(vres / 2, vres)
    for i in range(countofballs):
        spread = 180
        rand1 = random.randint(3 * spread, 5 * spread)
        rand2 = random.randint(-spread, spread)
        rand = rand1 if random.randint(0, 1) else rand2
        ball = Ball(Vector2(res[0] / 2, res[1] / 2), Vector2(cos(rand * pi / 180), sin(rand * pi / 180)), 5)
        balls.append(ball)
        del ball
    clock = pg.time.Clock()
    switch = 0
    draw_stack = list()
    controlled = list()
    while 1:
        beta = pg.mouse.get_pressed(3)[0]
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
        click = get_clicked(beta, pg.mouse.get_pressed(3)[0])
        Mouse = pg.mouse
        m_pos = Vector2(Mouse.get_pos())
        screen.fill((0, 0, 0))
        if switch:
            for line in draw_stack:
                line.p2 = m_pos
        for line in controlled:
            line.draw(screen)
        if click:
            if not switch:
                ln = Line(Vector2(Mouse.get_pos()), Vector2(Mouse.get_pos()))
                draw_stack.append(ln)
                controlled.append(ln)
                switch = 1
            elif switch:
                switch = 0
                for i in draw_stack:
                    draw_stack.remove(i)
        for ball in balls:
            ball.speed = 5
            objects = [screen_rect]
            for i in controlled:
                objects.append(i)
            ball.move(objects)
            ball.draw(screen)
        pg.display.update()


def game(screen: pg.Surface):
    res = screen.get_size()
    vres = Vector2(res)
    slider_length = Vector2(res[0] / 36, res[1] / 6)
    ball = Ball(Vector2(res[0] / 2, res[1] / 2), start_speed=5)
    screen_rect = Rectangle(vres / 2, vres)
    calm_zone = Rectangle(vres / 2, Vector2(vres.x - slider_length.x * 2, vres.y))
    calm_zone.color = Color(0, 155, 0, 150)
    sliderR = Rectangle(Vector2(vres.x - slider_length.x / 2, slider_length.y / 2), slider_length)
    camera = Camera(vres / 2, Vector2(1, 0), 100, 1000, 60)
    countL = 0
    countR = 0
    sliderR.color = Color(250, 100, 100)
    goal_rectL = Rectangle(Vector2(slider_length.x / 2, vres.y / 2), Vector2(slider_length.x, vres.y))
    goal_rectR = Rectangle(Vector2(vres.x - slider_length.x / 2, vres.y / 2), Vector2(slider_length.x, vres.y))
    points_textR = Text(f"Rightward guy points: {countR}", 30)
    points_textL = Text(f"Leftward guy points: {countL}", 30)
    points_textL.set_position(Vector2(slider_length.x, 0))
    ball.color = Color(255, 150, 100)
    speedR = 20
    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
        mpos = Vector2(pg.mouse.get_pos())
        screen.fill((0, 0, 0))
        sliderL = Rectangle(Vector2(slider_length.x / 2, mpos.y), slider_length, Color(255, 255, 255))
        sliderL.color = Color(100, 100, 250)
        y = sliderL.pos.y
        h = sliderL.size.y
        sliderL.pos.y = set_limit(y, h / 2, vres.y - h / 2)
        ball.move([sliderL, sliderR, screen_rect])
        if not inside(ball.pos, screen_rect):
            ball.respawn()
        if not inside(ball.pos, calm_zone):
            if ball.pos.x <= vres.x/2:
                countR += 1
            if ball.pos.x > vres.x/2:
                countL += 1
            ball.respawn()
        elif Belongs(ball.pos.x, sliderR.pos.x, 2 * vres.x / 3):
            v = sliderR.pos
            p = Vector2(ball.pos)
            d = ball.dir
            p1, p2 = screen_rect.get_side(0)
            p1, p2 = Vector2(p1.x - slider_length.x, p1.y), Vector2(p2.x - slider_length.x, p2.y)
            p_i = intersectRL(p, p + d, p1, p2)
            if p_i:
                u = Vector2(v.x, p_i.y)
                if not inside(u, sliderR):
                    u = (u - v).normalize()
                    sliderR.pos += speedR * u
            else:
                for i in range(0, screen_rect.get_point_count()):
                    p3, p4 = screen_rect.get_side(i)
                    p_i = intersectRL(p, p + d, p3, p4)
                    if p_i:
                        for i in range(1, screen_rect.get_point_count()):
                            p3, p4 = screen_rect.get_side(i)
                            r = reflect(p_i - p, p4 - p3)
                            pr = intersectRL(p_i, p_i + r, p1, p2)
                            if pr:
                                u = Vector2(v.x, pr.y)
                                if not inside(u, sliderR):
                                    u = (u - v).normalize()
                                    sliderR.pos += speedR * u
                        break
        text_width = get_text_width(points_textR.content, points_textR.char_size)
        points_textR.set_position(Vector2(vres.x - slider_length.x - text_width, 0))
        sliderR.pos.y = set_limit(sliderR.pos.y, h / 2, vres.y - h / 2)
        points_textL.set_text(f"Leftward guy points: {countL}")
        points_textR.set_text(f"Rightward guy points: {countR}")
        sbtext = Text(f"speed x{ball.speed/5}", 30)
        sbtext_width = get_text_width(sbtext.content, sbtext.char_size)
        sbtext.set_position(Vector2((vres.x - sbtext_width), vres.y)/2)
        sbtext.draw(screen)
        points_textL.draw(screen)
        points_textR.draw(screen)
        sliderL.draw(screen)
        sliderR.draw(screen)
        ball.draw(screen)
        pg.display.update()


def main(name, icon=None):
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((1920, 1080), SCALED)
    pg.display.set_caption(name)
    if type(icon) is pg.Surface:
        pg.display.set_icon(icon)
    test2(screen)


if __name__ == '__main__':
    ico = pg.image.load("img/ico.png")
    main('PyCharm', ico)
