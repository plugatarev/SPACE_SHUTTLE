import arcade
from random import  randint
from math import sin, cos, radians

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

def get_distanse(ob1, ob2):
    dx = ob2.x - ob1.x
    dy = ob2.y - ob1.y
    return  (dx ** 2 + dy ** 2) ** 0.5

class Apple:
    def __init__(self):
        self.size = randint(5,30)
        self.x = randint(self.size, SCREEN_WIDTH - self.size)
        self.y = randint(self.size, SCREEN_HEIGHT - self.size)
        self.color = arcade.color.BLUE

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.size, self.color)

    def is_collision(self, hero):
        r = get_distanse(self, hero)
        r2 = self.size + hero.size
        return r2 >= r


class Hero:
    def __init__(self):
        self.x = 1850
        self.y = 950
        self.dir = 0
        self.speed = 2
        self.size = 10

        self.color = arcade.color.HEART_GOLD

    def draw(self):
        dx = 80 * sin(radians(self.dir))
        dy = 80 * cos(radians(self.dir))
        arcade.draw_circle_filled(self.x, self.y, self.size, self.color)
        arcade.draw_line(self.x, self.y, self.x + 0.3 * dx, self.y + 0.3 * dy, [255,255,255], 4)

    def speed_up(self):
        if self.speed < 15:
            self.speed += 1

    def speed_down(self):
        if self.speed > -15:
            self.speed -= 1

    def turn_left(self):
        self.dir -= 10

    def turn_right(self):
        self.dir += 10

    def move(self, dir):
        dx = self.speed * sin(radians(self.dir))
        dy = self.speed * cos(radians(self.dir))
        self.x += dx
        self.y += dy
        # if dir == 'l':
        #     self.x -= 10
        # elif dir == 'r':
        #     self.x += 10
        # elif dir == 'u':
        #     self.y += 10
        # elif dir == 'd':
        #     self.y -= 10
pass


class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)


    def setup(self):
        # Настроить игру здесь
        self.hero = Hero()
        self.apple_list = []
        self.state = 'run'
        for i in range(randint(20, 30)):
            self.apple_list.append(Apple())
        pass

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        # Здесь код рисунка
        if self.state == 'run':
            self.hero.draw()
            for apple in self.apple_list:
                apple.draw()
        elif self.state == 'pause':
            pass
        elif self.state == 'game_over':
            self.hero.draw()
            for apple in self.apple_list:
                apple.draw()
            arcade.draw_text('Иди учись в АЭРО!!!', 200, 200, [200, 200, 200], 32)

    def update(self, delta_time):
        """ Здесь вся игровая логика и логика перемещения."""
        if self.state == 'run':
            self.hero.move('')
            for apple in self.apple_list:
                if apple.is_collision(self.hero):
                    self.state = 'game_over'

                # arcade.draw_text('Иди в АЭРО!!!', 122, 400, [200, 200, 200], 25, 300)

        pass

    def on_key_press(self, symbol: int, modifiers: int):
        if self.state == 'run':
            if symbol == arcade.key.LEFT:
                self.hero.move('l')
                self.hero.turn_left()
            elif symbol == arcade.key.RIGHT:
                self.hero.turn_right()
                self.hero.move('r')
            elif symbol == arcade.key.UP:
                self.hero.speed_up()
            elif symbol == arcade.key.DOWN:
                self.hero.speed_down()

def main():
    global IN_GAME
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()
    #arcade.schedule(on_draw, 1 / 80)


if __name__ == "__main__":
    main()





