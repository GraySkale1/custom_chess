import piece_class
import math
import pyglet
import levels
import chess

class scene():
    def __init__(self, screen:pyglet.window.Window, super_call:bool = False):
        if super_call != True:
            self.back_sprite = self.background(screen, "assets\\misc\\default_texture.png", fit=True)
        self.sprites = [self.back_sprite]

        self.screen = screen
        

    def on_mouse_press(self, x, y, button, modifiers):
        pass


    def move(self, sprite:pyglet.sprite.Sprite, pos:list):
        """places sprites with percentages instead of pixel position \n
        pos = [x, y]"""
        sprite.x = (self.screen.width - sprite.width) * pos[0]
        sprite.y = (self.screen.height - sprite.height) * pos[1]

        return sprite

    def background(self, img_PATH, fit=0):
        """Returns sprite correctly sized to fit window\n
        fit = 1 means that scale will not be changed"""
        background = pyglet.image.load(img_PATH)
        back_sprite = pyglet.sprite.Sprite(background)

        if fit == 1:
            back_sprite.scale.x = self.screen.width / back_sprite.width
            back_sprite.scale.y = self.screen.height / back_sprite.height
        else:
            back_sprite.scale = min(self.screen.width / back_sprite.width, self.screen.height / back_sprite.height)

        return self.move(self.screen, back_sprite, [0.5,0.5])
    

class main_game(scene):
    def __init__(self, screen:pyglet.window.Window):
        self.back_sprite = self.background(screen, "assets\\backgrounds\\chessboard.png")
        super().__init__(screen, super_call=True)

        self.spacing_scale = self.back_sprite.width / 8
        self.game_board = chess.board()
        self.game_board.reset()

        self.c_piece = None
        self.increment = 0

        #makes highlight tile correct size
        highlight = pyglet.image.load('assets\\misc\\yellow.jpg')
        self.highlight = pyglet.sprite.Sprite(highlight)
        highlight.scale_x = math.ceil(self.spacing_scale) / highlight.width
        highlight.scale_y = math.ceil(self.spacing_scale) / highlight.height

        self.game_sprites = self.piece_add(self.game_sprites)

    def pixel_to_index(self, pixel_pos: list):
        """converts pixel position on screen to position on chess board as list"""
        x1, y1 = pixel_pos
        x1 -= self.back_sprite.x
        y1 -= self.back_sprite.y
        p1 = y1 // self.spacing_scale
        p2 = x1 // self.spacing_scale
        return [7 - int(p1), int(p2)]

    def index_to_pixel(self, index_pos: list):
        """converts index position on board to pixel position screen"""
        p1, p2 = index_pos
        p1 = 7 - p1
        y1 = p1 * self.spacing_scale
        x1 = p2 * self.spacing_scale
        x1 += self.back_sprite.x
        y1 += self.back_sprite.y
        return [int(x1), int(y1)]
    
    def piece_add(self, game_sprites_list:list):
        game_sprites_list = [game_sprites_list[0]]
        game_sprites_list.append(self.game_sprites)
        for pos in self.game_board.piece_pos:
            x,y = pos
            px,py = self.index_to_pixel(pos)
            if self.game_board.chess_board[x][y] != 0:
                image = pyglet.image.load(self.game_board.chess_board[x][y].sprite())
                sprite = pyglet.sprite.Sprite(image, x=px, y=py)
                sprite.scale = math.ceil(self.spacing_scale) / sprite.width
                game_sprites_list.append(sprite)
        return game_sprites_list
    
    def on_mouse_press(self, x, y, button, modifiers):
        p1, p2 = self.pixel_to_index([x,y])

        current_piece = self.game_board.chess_board[p1][p2]
        if self.increment == 0:
            past_piece = None
            self.increment += 1
            self.highlight.position = (self.index_to_pixel([p1,p2])[0], self.index_to_pixel([p1,p2])[1], self.highlight.z)
            game_sprites.insert(1, self.highlight)

        elif self.increment % 2 == 0:
            if past_piece != 0 and current_piece != 0:
                exe = 1
            else:
                exe = 0

            vec = self.game_board._vector(self.past, self.pixel_to_index([x,y]))
            if issubclass(type(past_piece), piece_class.piece):
                move = chess.movement(start=self.past, vector=vec, exe=exe, team=(past_piece.team))
                self.game_board.execute(move)
            if self.highlight in game_sprites:
                game_sprites.remove(self.highlight)
            game_sprites = self.piece_add(game_sprites)
        else:
            self.highlight.position = (self.index_to_pixel([p1,p2])[0], self.index_to_pixel([p1,p2])[1], self.highlight.z)
            game_sprites.insert(1, self.highlight)
                
        past_piece = current_piece
        self.increment += 1
        

        self.past = self.pixel_to_index([x,y])