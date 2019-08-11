import arcade
from random import  randint, choice, random
from math import sin, cos, radians

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

img_background = arcade.load_texture('img/background.jpg')
img_planet = arcade.load_texture('img/planet_bc.png')
img_space_suttle = arcade.load_texture('img/rokets.png')
img_planet_list = []
for i in range(4):
    filename = 'img/planet{}.png'.format(i + 1)
    img_planet_list.append(arcade.load_texture(filename))


def get_distanse(ob1, ob2):
    dx = ob2.x - ob1.x
    dy = ob2.y - ob1.y
    return (dx ** 2 + dy ** 2) ** 0.5

# class Background:
#     def __init__(self):
#         # self.img =
#         pass
#
#     def draw(self):
#


class Planet:
    def __init__(self):
        self.size = randint(60, 100)
        self.x = randint(self.size, SCREEN_WIDTH - self.size)
        self.y = randint(self.size, SCREEN_HEIGHT - self.size)
        self.speed = randint(0, 10) / 40
        self.dir = randint(0, 359)
        self.color = arcade.color.BLUE
        self.img = choice(img_planet_list)

    def draw(self):
        # arcade.draw_circle_filled(self.x, self.y, self.size, self.color)
        arcade.draw_texture_rectangle(self.x, self.y, self.size, self.size, self.img)

    def move(self):
        dx = self.speed * sin(radians(self.dir))
        dy = self.speed * cos(radians(self.dir))
        self.x += dx
        self.y += dy

    def is_collision(self, hero):
        r = get_distanse(self, hero)
        r2 = self.size / 3 + hero.size / 2
        return r2 >= r

class Hero:
    def __init__(self):
        self.x = 1850
        self.y = 950
        self.dir = 210
        self.speed = 2
        self.speed_rotation = 0
        self.fuel = 100
        self.fuel_prec = 0.1
        self.size = 60
        self.color = arcade.color.HEART_GOLD

    def draw(self):
        arcade.draw_texture_rectangle(self.x, self.y,
                                      self.size * 0.8, self.size * 1.5,
                                      img_space_suttle, - self.dir)
        # dx = 80 * sin(radians(self.dir))
        # dy = 80 * cos(radians(self.dir))
        # arcade.draw_circle_filled(self.x, self.y, self.size, self.color)
        # arcade.draw_line(self.x, self.y, self.x + 0.3 * dx, self.y + 0.3 * dy, [255, 255, 255], 4)

    def update(self):
        if self.fuel >= self.fuel_prec:
            self.fuel -= self.fuel_prec
        else:
            self.speed_rotation = 0


    def speed_up(self):
        if self.speed < 4 and self.fuel > 0:
            self.speed += 0.25

    def speed_down(self):
        if self.speed >= 1 and self.fuel > 0:
            self.speed -= 0.4

    def rotation_left(self):
        if self.fuel > 0:
            self.speed_rotation = -0.5

    def rotation_right(self):
        if self.fuel > 0:
            self.speed_rotation = 0.5

    def rotation_stop(self):
        self.speed_rotation = 0

    def turn_left(self):
        if self.fuel > 0:
            self.dir -= 10

    def turn_right(self):
        if self.fuel > 0:
            self.dir += 10

    def move(self):
        self.dir += self.speed_rotation
        dx = self.speed * sin(radians(self.dir))
        dy = self.speed * cos(radians(self.dir))
        self.x += dx
        self.y += dy

    def is_crash(self):
        out_x = not(0 < self.x < SCREEN_WIDTH)
        out_y = not(0 < self.y < SCREEN_HEIGHT)
        return out_x or out_y


class MyGame(arcade.Window):
    """ Главный класс приложения. """
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        # Настроить игру здесь
        self.hero = Hero()
        self.planet = Planet()
        self.planet.img = img_planet
        self.planet_list = []
        self.state = 'run'
        self.step = 0
        self.telemetry = ''
        for i in range(randint(20, 30)):
            self.planet_list.append(Planet())

    def draw_telemetry(self):
        if self.step % 20 == 0:
            self.telemetry = 'fuel: {} %\n'.format(round(self.hero.fuel, 1)) + \
                             'speed: {} m/s\n'.format(round(self.hero.speed * 987, 1)) + \
                             'X: {} m\n'.format(round(self.hero.x, 1))

        arcade.draw_text(self.telemetry, 10, SCREEN_HEIGHT - 100
                         , [200, 200, 200], 30,
                         width=1300, align="left", anchor_x="left", anchor_y="center")


    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, img_background)
        if self.state == 'run':
            self.hero.draw()
            for apple in self.planet_list:
                apple.draw()
            self.planet.draw()
            self.draw_telemetry()
        elif self.state == 'pause':
            pass
        elif self.state == 'win':
            for apple in self.planet_list:
                apple.draw()
            self.planet.draw()
            arcade.draw_text('Победа вместо обеда!!!',
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
                             , [200, 200, 200], 100,
                             width=1300, align="center", anchor_x="center", anchor_y="center")

        elif self.state == 'game_over':
            self.hero.draw()
            self.planet.draw()
            for apple in self.planet_list:
                apple.draw()
            arcade.draw_text('Иди учись в АЭРО!!!', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
                             , [200, 200, 200], 100,
                             width=1200, align="center", anchor_x="center", anchor_y="center")

    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        if self.state == 'run':
            self.step += 1
            self.hero.move()
            self.hero.update()
            if self.hero.is_crash():
                self.state = 'game_over'
            if self.planet.is_collision(self.hero):
                self.state = 'win'
            for planet in self.planet_list:
                planet.move()
                if planet.is_collision(self.hero) :
                    self.state = 'game_over'


    def on_key_press(self, symbol: int, modifiers: int):
        if self.state == 'run':
            if symbol == arcade.key.LEFT:
                self.hero.move()
                self.hero.rotation_left()
            elif symbol == arcade.key.RIGHT:
                self.hero.rotation_right()
                self.hero.move()
            elif symbol == arcade.key.UP:
                self.hero.speed_up()
            elif symbol == arcade.key.DOWN:
                self.hero.speed_down()

    def on_key_release(self, symbol: int, modifiers: int):
        if self.state == 'run':
            if symbol == arcade.key.LEFT:
                self.hero.rotation_stop()
            elif symbol == arcade.key.RIGHT:
                self.hero.rotation_stop()

def main():
    global IN_GAME
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
