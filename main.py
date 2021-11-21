import pygame
import typing


pygame.init()
pygame.font.init()


class Canva:
    pass


class MenuItem(pygame.sprite.Sprite):
    text: str
    text_rendered: pygame.Surface
    selected: bool


class Menu:
    padding = 5
    font: pygame.font.Font = pygame.font.SysFont('Times New Roman', 40)
    font_color = (0, 0, 0)
    bg_hid_color = (255, 255, 255)

    def __init__(self, pos):    
        self.surface: pygame.Surface
        self.rect: pygame.Rect
        self.pos = pos
        self.changes = False

        options = ['line', 'line', "ola", "hei", 'delo', 'i']
        self.options: typing.List[MenuItem] = list()

        for option in options:
            mi = MenuItem()
            mi.text = option
            mi.text_rendered = self.font.render(option, True, self.font_color)
            self.options.append(mi)
        
        self.plot()
    
    def select(self, option_sel):
        self.changes = True
        self.surface.fill((0, 0, 0, 0))

        for option in self.options:
            option.selected = False
            if option is option_sel:
                pygame.draw.rect(self.surface, (0, 0, 0, 100), option.rect)
                option.selected = True
            self.surface.blit(option.image, option.rect)
    
    def draw_image(self):
        if not self.changes:
            return
        self.surface.fill((0, 0, 0, 0))
        for option in self.options:
            self.surface.blit(option.image, (option.rect.x, option.rect.y))
        self.changes = False
    
    def mouse_movement(self, pos):
        relative_pos = pygame.math.Vector2(pos) - pygame.math.Vector2(self.pos)
        for option in self.options:
            if option.rect.collidepoint(relative_pos):
                self.select(option)
                break

    def plot(self):
        max_x = max([x.text_rendered.get_width() for x in self.options])+2*self.padding
        current_y = 0
        for option in self.options:
            option.image = pygame.Surface((max_x, option.text_rendered.get_height()+2*self.padding), flags=pygame.SRCALPHA)
            option.image.blit(option.text_rendered, (max_x//2-option.text_rendered.get_width()//2, self.padding))

            option.rect = pygame.Rect((0, current_y), option.image.get_size())
            pygame.draw.rect(option.image, self.font_color, ((0, 0), option.rect.size), width=1)
            current_y += option.image.get_height()

        self.surface = pygame.Surface((max_x, current_y), flags=pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect = self.rect.move(self.pos)

        self.changes = True

        self.draw_image()


class AppManager:
    def __init__(self, width, heigth) -> None:
        self.screen = pygame.display.set_mode((width, heigth))
        self.menu = Menu((0, 0))
        self.canva = Canva()
    
    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.fill(pygame.Color('white'))
            self.screen.blit(self.menu.surface, self.menu.pos)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION:
                    if self.menu.rect.collidepoint(event.pos):
                        self.menu.mouse_movement(event.pos)
                    else:
                        self.menu.draw_image()
            
            clock.tick(30)


x, y = 900, 500

app_manager = AppManager(x, y)

app_manager.run()
