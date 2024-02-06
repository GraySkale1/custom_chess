import piece_class
import assets.Scenes.game_scene as chess_game
import assets.Scenes.end_scene as end_scene
import pyglet
import levels
import chess

display = pyglet.canvas.Display()
screen = display.get_default_screen()

WIDTH = 500
HEIGHT = 500



game = pyglet.window.Window(width=WIDTH, height=HEIGHT)

game_scene = chess_game.main_game(screen=game)
current_scene = game_scene


@game.event
def on_mouse_press(x, y, button, modifiers):
    global current_scene
    current_scene.on_mouse_press(x,y,button,modifiers)


@game.event
def on_draw():
    global current_scene
    game.clear()
    for sprite in current_scene.on_draw():
        sprite.draw()

    possible_winner = game_scene.game_board.win_condition(extra=True)

    if possible_winner != False:
        current_scene = end_scene.winner(screen=game, winner_name=possible_winner)




pyglet.app.run()
