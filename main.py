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
    scroll_bar_width = 10

    def __init__(self, pos, dim: tuple): 
        self.image: pygame.Surface
        self.surface: pygame.Surface
        self.rect: pygame.Rect
        self.relative_rect: pygame.Rect
        self.scroll_bar: pygame.Rect
        self.line_width = 1
        self.no_scroll = False
        self.pos = pos
        self.changes = False
        self.dim = dim

        options = [random.choice(['line', 'line', "ola", "hei", 'delo', 'i']) for i in range(60)]
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
                self.relative_rect.move_ip(0, -20)
            if self.relative_rect.bottom < self.rect.h:
                self.relative_rect.bottom = self.rect.h
        else:
            if self.relative_rect.y < 0:
                self.relative_rect.move_ip(0, 20)
            if self.relative_rect.y > 0:
                self.relative_rect.y = 0
        
        self.mouse_movement(pos)

        self.scroll_bar.y = -int(((self.relative_rect.y-self.rect.y)/self.relative_rect.h)*self.rect.h)
        
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

        pygame.draw.rect(self.image, (0, 0, 0), (self.rect.w-self.scroll_bar_width-self.line_width*2, 0, self.scroll_bar_width+self.line_width*2, self.rect.h), width=self.line_width)
        pygame.draw.rect(self.image, (0, 0, 0), self.scroll_bar, border_radius=3)
        pygame.draw.rect(self.image, (0, 0, 0), self.rect, width=self.line_width, border_radius=2)

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
            pygame.draw.rect(option.image, self.font_color, ((0, 0), option.rect.size), width=self.line_width)
            current_y += option.image.get_height()

        self.surface = pygame.Surface((max_x, current_y), flags=pygame.SRCALPHA)
        self.relative_rect = self.surface.get_rect()
        
        if self.dim[0] is None and self.dim[1] is None:
            self.image = pygame.Surface((max_x+self.scroll_bar_width+self.line_width, current_y), flags=pygame.SRCALPHA)
        elif self.dim[0] is None:
            self.image = pygame.Surface((max_x+self.scroll_bar_width+self.line_width, self.dim[1]), flags=pygame.SRCALPHA)
        elif self.dim[1] is None:
            self.image = pygame.Surface((self.dim[0], current_y), flags=pygame.SRCALPHA)
        else:
            self.image = pygame.Surface((self.dim[0], self.dim[1]), flags=pygame.SRCALPHA)
        
        self.rect = self.image.get_rect()
        print(self.rect, max_x, self.scroll_bar_width)
        self.rect.x, self.rect.y = self.pos

        self.scroll_bar = pygame.Rect((self.rect.w-self.scroll_bar_width-self.line_width, int((self.relative_rect.y-self.rect.y)/self.relative_rect.h))
                                      ,(self.scroll_bar_width, int(self.rect.h/self.relative_rect.h*self.rect.h)))
        
        print(self.scroll_bar)
        print(self.rect)

        if self.rect.h > self.relative_rect.h:
            self.no_scroll = True

        self.changes = True

        self.draw_image()


class AppManager:
    def __init__(self, width, height) -> None:
        self.screen = pygame.display.set_mode((width, height))
        self.menu = Menu((0, 0), (None, 200))
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
                    self.menu.mouse_movement(event.pos)
            
            clock.tick(60)


x, y = 900, 500

app_manager = AppManager(x, y)

app_manager.run()
