import pygame
import settings

from sprites.paddle import Player, Opponent
from sprites.ball import Ball
 
class Game:
    def __init__(self):
        #init
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.running = True
        self.clock = pygame.time.Clock()

        #groups
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()

        #sprites
        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball((self.all_sprites), self.paddle_sprites, self.__update_score)
        self.opponent = Opponent((self.all_sprites, self.paddle_sprites), self.ball)

        #score
        self.score = {"player": 0, "opponent": 0}
        self.font = pygame.font.Font(None, 160)

    def __display_score(self):
        #player
        player_surf = self.font.render(str(self.score["player"]), True, settings.COLORS["bg detail"])
        player_rect = player_surf.get_frect(center = (settings.WINDOW_WIDTH / 2 + 100, settings.WINDOW_HEIGHT / 2))
        self.display_surface.blit(player_surf, player_rect)

        #opponent
        opponent_surf = self.font.render(str(self.score["opponent"]), True, settings.COLORS["bg detail"])
        opponent_rect = opponent_surf.get_frect(center = (settings.WINDOW_WIDTH / 2 - 100, settings.WINDOW_HEIGHT / 2))
        self.display_surface.blit(opponent_surf, opponent_rect)

        #field (line) separator
        pygame.draw.line(self.display_surface, settings.COLORS["bg detail"], (settings.WINDOW_WIDTH / 2, 0), (settings.WINDOW_WIDTH / 2, settings.WINDOW_HEIGHT), 6)

    def __update_score(self, side):
        self.score[side] += 1

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.display_surface.fill(settings.COLORS["bg"])

            self.__display_score()
            self.all_sprites.draw(self.display_surface)
            self.all_sprites.update(dt)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()

    
