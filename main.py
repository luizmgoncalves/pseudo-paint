import pygame
import typing
import random


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

    def __init__(self, pos, dim: tuple): 
        self.image: pygame.Surface
        self.surface: pygame.Surface
        self.rect: pygame.Rect
        self.relative_rect: pygame.Rect
        self.no_scroll = False
        self.pos = pos
        self.changes = False
        self.dim = dim

        options = [random.choice(['line', 'line', "ola", "hei", 'delo', 'i']) for i in range(20)]
        self.options: typing.List[MenuItem] = list()

        for option in options:
            mi = MenuItem()
            mi.text = option
            mi.text_rendered = self.font.render(option, True, self.font_color)
            mi.selected = False
            self.options.append(mi)
        
        self.plot()
    
    def scroll(self, pos, down=True):
        if self.no_scroll:
            return 
        
        if down:
            if self.relative_rect.bottom > self.rect.h:
                self.relative_rect.move_ip(0, -7)
            if self.relative_rect.bottom < self.rect.h:
                self.relative_rect.bottom = self.rect.h
        else:
            if self.relative_rect.y < 0:
                self.relative_rect.move_ip(0, 7)
            if self.relative_rect.y > 0:
                self.relative_rect.y = 0
        
        self.mouse_movement(pos)
        
        self.changes = True
        self.draw_image()

    
    def draw_image(self):
        if not self.changes:
            return
        self.surface.fill((0, 0, 0, 0))
        self.image.fill((0, 0, 0, 0))
        
        for option in self.options:
            if option.selected:
                pygame.draw.rect(self.surface, (0, 0, 0, 100), option.rect)
            self.surface.blit(option.image, option.rect)
        
        self.image.blit(self.surface, self.relative_rect)

        self.changes = False
    
    def mouse_movement(self, pos):
        relative_pos = pygame.math.Vector2(pos) - pygame.math.Vector2(self.pos) - pygame.math.Vector2(self.relative_rect.x, self.relative_rect.y)
        for option in self.options:
            if option.rect.collidepoint(relative_pos):
                option.selected = True
            else:
                option.selected = False
        self.changes = True
        self.draw_image()

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
        self.relative_rect = self.surface.get_rect()

        if self.dim[0] is None:
            self.image = pygame.Surface((max_x, self.dim[1]), flags=pygame.SRCALPHA)
        else:
            self.image = pygame.Surface(self.dim, flags=pygame.SRCALPHA)
        
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

        if self.rect.h > self.relative_rect.h:
            self.no_scroll = True

        self.changes = True

        self.draw_image()


class AppManager:
    def __init__(self, width, height) -> None:
        self.screen = pygame.display.set_mode((width, height))
        self.menu = Menu((0, 0), (None, height))
        self.canva = Canva()
    
    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.fill(pygame.Color('white'))
            self.screen.blit(self.menu.image, self.menu.pos)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu.rect.collidepoint(event.pos):
                        if event.button == 4:
                            self.menu.scroll(event.pos, False)
                        elif event.button == 5:
                            self.menu.scroll(event.pos)
                    
                if event.type == pygame.MOUSEMOTION:
                    if self.menu.rect.collidepoint(event.pos):
                        self.menu.mouse_movement(event.pos)
                    else:
                        self.menu.draw_image()
            
            clock.tick(60)


x, y = 900, 500

app_manager = AppManager(x, y)

app_manager.run()
