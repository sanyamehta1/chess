"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""
import pygame as p
import chess_engine

WIDTH = HEIGHT = 512
DIMENSION = 8  # a chess_local board has dimension 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animations later on
IMAGES = {}

"""
Initialize a global dictionary of images. This will be called exactly once from main.
"""


def load_images():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
        # we can now access an image by saying IMAGES["wp"]


"""
The main driver for our code. This will handle user input and updating the graphics.
"""


def main():
    p.init()  # initializing pygame
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chess_engine.GameState()
    load_images()  # we only do this once, before the while loop
    running = True
    sq_selected = ()   # no square is selected, keep track of the last click of the user
    player_clicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)]

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sq_selected == (row, col):  # the user clicked the same square twice
                    sq_selected = ()  # deselect
                    player_clicks = []  # clear player clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)  # append for both 1st and 2nd clicks
                if len(player_clicks) == 2:  # after 2nd square is selected
                    move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    gs.make_move(move)
                    sq_selected = ()  # reset user clicks
                    player_clicks = []

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


"""
Responsible for all the graphics within a current game state.
"""


def draw_game_state(screen, gs):
    draw_board(screen)  # draw squares on the board
    # add in piece highlighting or move suggestions (later)
    draw_pieces(screen, gs.board)  # draw pieces on top of those squares


"""
Draw squares on the board. The top left square is always light.
"""


def draw_board(screen):
    colors = [p.Color("white"), p.Color("pink")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Draw the pieces on the board using the current GameState.board
"""


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not an empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()

main()
