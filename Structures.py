import pygame


class UnitObject(pygame.sprite.Sprite):

    def __init__(self, x, y, image_string):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_string)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 2


class Structure(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.group_tiles = pygame.sprite.Group()

    def add_tiles(self, tiles):
        [self.group_tiles.add(unit) for unit in tiles]

    def draw(self, screen):
        self.group_tiles.draw(screen)

    def motion(self, gw):
        stop_flag = False
        for individual_block in self.group_tiles:
            next_y_loc = individual_block.rect.y + individual_block.vel_y
            if next_y_loc + individual_block.rect.height > gw.screen_height and gw.flying:
                stop_flag = True
                break
        if stop_flag:
            self.stop(gw)
        else:
            for individual_block in self.group_tiles:
                individual_block.rect.y += individual_block.vel_y

    def stop(self, gw):
        gw.spawn = True
        gw.flying = False
        for individual_block in self.group_tiles:
            individual_block.vel_y = 0
            gw.bottom_structure.add(individual_block)

    def collision_detection(self, gw):
        collide_flag = False
        for individual_block in self.group_tiles:
            if pygame.sprite.spritecollide(individual_block, gw.bottom_structure, False):
                collide_flag = True
                break
        if collide_flag:
            for individual_block in self.group_tiles:
                individual_block.rect.y -= individual_block.vel_y
            self.stop(gw)

    def move_right(self, screen_width, bottom_structure):
        move = True
        rollback_move = False

        for individual_block in self.group_tiles:
            if individual_block.rect.x + individual_block.rect.width == screen_width:
                move = False
                break

        if move:
            for individual_block in self.group_tiles:
                individual_block.rect.x += 20

        for individual_block in self.group_tiles:
            if pygame.sprite.spritecollide(individual_block, bottom_structure, False):
                rollback_move = True
                break

        if rollback_move:
            for individual_block in self.group_tiles:
                individual_block.rect.x -= 20

    def move_left(self, bottom_structure):
        move = True
        rollback_move = False

        for individual_block in self.group_tiles:
            if individual_block.rect.x == 0:
                move = False
                break

        if move:
            for individual_block in self.group_tiles:
                individual_block.rect.x -= 20

        for individual_block in self.group_tiles:
            if pygame.sprite.spritecollide(individual_block, bottom_structure, False):
                rollback_move = True
                break

        if rollback_move:
            for individual_block in self.group_tiles:
                individual_block.rect.x += 20

    def rotate(self, gw):
        gw.structure_in_air.rotate_structure(self)

    def come_down_fast(self, screen_height):
        y_pos = []
        [y_pos.append(individual_object.rect.y) for individual_object in self.group_tiles]
        y_pos.sort()
        y_left_to_cover_ratio = (screen_height - y_pos[3]) % 10
        for individual_object in self.group_tiles:
            individual_object.rect.y += y_left_to_cover_ratio
        for individual_object in self.group_tiles:
            individual_object.vel_y = 10


class StructureLine(Structure):

    def __init__(self, image_string):
        Structure.__init__(self)
        self.rotate_type = 1

        normal_list = [UnitObject(120, 0, image_string),
                       UnitObject(140, 0, image_string),
                       UnitObject(160, 0, image_string),
                       UnitObject(180, 0, image_string)]
        super(StructureLine, self).add_tiles(normal_list)

    def rotate_structure(self, structure_in_air):
        x_pos = []
        y_pos = []
        [x_pos.append(individual_block.rect.x) for individual_block in structure_in_air.group_tiles]
        [y_pos.append(individual_block.rect.y) for individual_block in structure_in_air.group_tiles]
        x_pos.sort()
        y_pos.sort()
        if self.rotate_type == 1 and y_pos[0] + 80 <= 600:
            self.rotate_type = 2
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.x == x_pos[1]:
                    individual_block.rect.x -= 20
                    individual_block.rect.y += 20
                elif individual_block.rect.x == x_pos[2]:
                    individual_block.rect.x -= 40
                    individual_block.rect.y += 40
                elif individual_block.rect.x == x_pos[3]:
                    individual_block.rect.x -= 60
                    individual_block.rect.y += 60

        elif self.rotate_type == 2 and x_pos[0] + 80 <= 320:
            self.rotate_type = 1
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.y == y_pos[1]:
                    individual_block.rect.x += 20
                    individual_block.rect.y -= 20
                elif individual_block.rect.y == y_pos[2]:
                    individual_block.rect.x += 40
                    individual_block.rect.y -= 40
                elif individual_block.rect.y == y_pos[3]:
                    individual_block.rect.x += 60
                    individual_block.rect.y -= 60

        elif self.rotate_type == 2 and x_pos[0] + 80 > 320:
            self.rotate_type = 1
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.y == y_pos[1]:
                    individual_block.rect.x -= 20
                    individual_block.rect.y -= 20
                elif individual_block.rect.y == y_pos[2]:
                    individual_block.rect.x -= 40
                    individual_block.rect.y -= 40
                elif individual_block.rect.y == y_pos[3]:
                    individual_block.rect.x -= 60
                    individual_block.rect.y -= 60


class StructureSquare(Structure):

    def __init__(self, image_string):
        Structure.__init__(self)
        self.rotate_type = 1

        normal_list = [UnitObject(140, 0, image_string),
                       UnitObject(140, 20, image_string),
                       UnitObject(160, 0, image_string),
                       UnitObject(160, 20, image_string)]
        super(StructureSquare, self).add_tiles(normal_list)

    def rotate_structure(self, structure_in_air):
        pass


class StructureZ(Structure):

    def __init__(self, image_string):
        Structure.__init__(self)
        self.rotate_type = 1

        normal_list = [UnitObject(120, 0, image_string),
                       UnitObject(140, 0, image_string),
                       UnitObject(140, 20, image_string),
                       UnitObject(160, 20, image_string)]
        super(StructureZ, self).add_tiles(normal_list)

    def rotate_structure(self, structure_in_air):
        x_pos = []
        y_pos = []
        [x_pos.append(individual_block.rect.x) for individual_block in structure_in_air.group_tiles]
        [y_pos.append(individual_block.rect.y) for individual_block in structure_in_air.group_tiles]
        x_pos.sort()
        y_pos.sort()
        if self.rotate_type == 1 and y_pos[0] + 60 <= 600:
            self.rotate_type = 2
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.x == x_pos[0]:
                    individual_block.rect.y += 20
                elif individual_block.rect.x == x_pos[3]:
                    individual_block.rect.x -= 40
                    individual_block.rect.y += 20

        elif self.rotate_type == 2 and x_pos[0] + 60 <= 320:
            self.rotate_type = 1
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.y == y_pos[1] and individual_block.rect.x == x_pos[0]:
                    individual_block.rect.y -= 20
                elif individual_block.rect.y == y_pos[3]:
                    individual_block.rect.x += 40
                    individual_block.rect.y -= 20

        elif self.rotate_type == 2 and x_pos[0] + 60 > 320:
            self.rotate_type = 1
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.y == y_pos[0]:
                    individual_block.rect.x -= 40
                elif individual_block.rect.y == y_pos[3]:
                    individual_block.rect.y -= 40


class StructureT(Structure):

    def __init__(self, image_string):
        Structure.__init__(self)
        self.rotate_type = 1

        normal_list = [UnitObject(120, 20, image_string),
                       UnitObject(140, 20, image_string),
                       UnitObject(160, 20, image_string),
                       UnitObject(140, 0, image_string)]
        super(StructureT, self).add_tiles(normal_list)

    def rotate_structure(self, structure_in_air):
        x_pos = []
        y_pos = []
        [x_pos.append(individual_block.rect.x) for individual_block in structure_in_air.group_tiles]
        [y_pos.append(individual_block.rect.y) for individual_block in structure_in_air.group_tiles]
        x_pos.sort()
        y_pos.sort()
        if self.rotate_type == 1 and y_pos[0] + 60 <= 600:
            self.rotate_type = 2
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.x == x_pos[0]:
                    individual_block.rect.y += 20
                    individual_block.rect.x += 20

        elif self.rotate_type == 2 and x_pos[0] >= 20:
            self.rotate_type = 3
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.y == y_pos[0]:
                    individual_block.rect.x -= 20
                    individual_block.rect.y += 20

        elif self.rotate_type == 2 and x_pos[0] < 20:
            self.rotate_type = 3
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.y == y_pos[0]:
                    individual_block.rect.x += 40
                    individual_block.rect.y += 20
                if individual_block.rect.y == y_pos[3]:
                    individual_block.rect.x += 20

        elif self.rotate_type == 3:
            self.rotate_type = 4
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.x == x_pos[3]:
                    individual_block.rect.x -= 20
                    individual_block.rect.y -= 20

        elif self.rotate_type == 4 and x_pos[0] + 60 <= 320:
            self.rotate_type = 1
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.y == y_pos[3]:
                    individual_block.rect.x += 20
                    individual_block.rect.y -= 20

        elif self.rotate_type == 4 and x_pos[0] + 60 > 320:
            self.rotate_type = 1
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.y == y_pos[0]:
                    individual_block.rect.x -= 20
                elif individual_block.rect.y == y_pos[3]:
                    individual_block.rect.x -= 40
                    individual_block.rect.y -= 20


class StructureL(Structure):

    def __init__(self, image_string):
        Structure.__init__(self)
        self.rotate_type = 1

        normal_list = [UnitObject(120, 20, image_string),
                       UnitObject(140, 20, image_string),
                       UnitObject(160, 20, image_string),
                       UnitObject(120, 0, image_string)]
        super(StructureL, self).add_tiles(normal_list)

    def rotate_structure(self, structure_in_air):
        x_pos = []
        y_pos = []
        [x_pos.append(individual_block.rect.x) for individual_block in structure_in_air.group_tiles]
        [y_pos.append(individual_block.rect.y) for individual_block in structure_in_air.group_tiles]
        x_pos.sort()
        y_pos.sort()
        if self.rotate_type == 1 and y_pos[0] + 60 <= 600:
            self.rotate_type = 2
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.x == x_pos[2]:
                    individual_block.rect.y += 20
                    individual_block.rect.x -= 20
                if individual_block.rect.x == x_pos[3]:
                    individual_block.rect.y -= 20
                    individual_block.rect.x -= 20

        elif self.rotate_type == 2 and x_pos[0] >= 20:
            self.rotate_type = 3
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.y == y_pos[2]:
                    individual_block.rect.x += 20
                if individual_block.rect.y == y_pos[3]:
                    individual_block.rect.x -= 20
                    individual_block.rect.y -= 40

        elif self.rotate_type == 2 and x_pos[0] < 20:
            self.rotate_type = 3
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.y == y_pos[2]:
                    individual_block.rect.x += 40
                if individual_block.rect.y == y_pos[3]:
                    individual_block.rect.x += 40
                    individual_block.rect.y -= 40

        elif self.rotate_type == 3:
            self.rotate_type = 4
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.x == x_pos[0]:
                    individual_block.rect.x += 40
                    individual_block.rect.y -= 20
                if individual_block.rect.y == y_pos[3]:
                    individual_block.rect.y -= 60

        elif self.rotate_type == 4 and x_pos[0] + 80 <= 320:
            self.rotate_type = 1
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.x == x_pos[0]:
                    individual_block.rect.x += 60
                if individual_block.rect.y == y_pos[0]:
                    individual_block.rect.y += 40
                    individual_block.rect.x += 20

        elif self.rotate_type == 4 and x_pos[0] + 80 > 320:
            self.rotate_type = 1
            for individual_block in structure_in_air.group_tiles:
                if individual_block.rect.y == y_pos[0]:
                    individual_block.rect.x -= 40
                    individual_block.rect.y += 40
                elif individual_block.rect.y == y_pos[1]:
                    individual_block.rect.x -= 40
