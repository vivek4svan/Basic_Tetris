import sys
import os
import pygame
import Structures
from random import randint


class GameWorld(pygame.sprite.Sprite):

    def __init__(self, screen_width, screen_height, fps):
        pygame.sprite.Sprite.__init__(self)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps
        self.spawn = True
        self.flying = False
        self.game_lost = False
        self.pause = False
        self.score = 0
        self.structure_in_air = None
        self.bottom_structure = pygame.sprite.Group()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1300, 300)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        self.clock = pygame.time.Clock()
        pygame.init()

    def run(self):

        while not self.game_lost:
            if not self.pause:
                pygame.display.flip()
                self.screen.fill((0, 0, 0))
                self.check_loose()
                self._spawn_new_blocks()
                self.structure_in_air.motion(self)
                self.structure_in_air.collision_detection(self)
                self.structure_in_air.draw(self.screen)
                self.bottom_structure.draw(self.screen)
                self.check_for_clear()
                self._process()
                self.clock.tick(self.fps)
            else:
                self.pause_process()

        while self.game_lost:
            pygame.display.flip()
            self.screen.fill((100, 0, 100))
            self.bottom_structure.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(self.fps)

    def check_loose(self):
        for individual_block in self.bottom_structure:
            if individual_block.rect.y == 0:
                self.game_lost = True

    def _process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.structure_in_air.move_right(self.screen_width, self.bottom_structure)
                elif event.key == pygame.K_LEFT:
                    self.structure_in_air.move_left(self.bottom_structure)
                if event.key == pygame.K_SPACE:
                    self.structure_in_air.rotate(self)
                elif event.key == pygame.K_DOWN:
                    self.structure_in_air.come_down_fast(self.screen_height)
                elif event.key == pygame.K_p:
                    self.pause = not self.pause

        # keys = pygame.key.get_pressed()
        #
        # if keys[pygame.K_RIGHT]:
        #     self.structure_in_air.move_right(self.screen_width, self.bottom_structure)
        # elif keys[pygame.K_LEFT]:
        #     self.structure_in_air.move_left(self.bottom_structure)

    def pause_process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause = not self.pause

    def _spawn_new_blocks(self):
        if self.spawn and not self.flying:
            # check_for_clear()
            structure_type = randint(1, 5)
            self.spawn = False
            self.flying = True
            if structure_type == 1:
                self.structure_in_air = Structures.StructureLine("./images/unit_square_01.png")
            elif structure_type == 2:
                self.structure_in_air = Structures.StructureSquare("./images/unit_square_01.png")
            elif structure_type == 3:
                self.structure_in_air = Structures.StructureZ("./images/unit_square_01.png")
            elif structure_type == 4:
                self.structure_in_air = Structures.StructureT("./images/unit_square_01.png")
            elif structure_type == 5:
                self.structure_in_air = Structures.StructureL("./images/unit_square_01.png")

    def check_for_clear(self):
        rows_to_be_deleted = []
        for y_pixel_pos in range(580, -1, -20):
            counter = 0
            for individual_object in self.bottom_structure:
                if individual_object.rect.y == y_pixel_pos:
                        counter += 1
            if counter == 16:
                rows_to_be_deleted.append(y_pixel_pos)

        rows_to_be_deleted.reverse()

        for y_clear_row in rows_to_be_deleted:
            for individual_object in self.bottom_structure:
                if individual_object.rect.y == y_clear_row:
                    self.bottom_structure.remove(individual_object)
            for individual_object in self.bottom_structure:
                if individual_object.rect.y < y_clear_row:
                    individual_object.rect.y += 20
