import pygame
import sys

from game_functionality.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SQSIZE
from game_functionality.game import Game
from game_functionality.square import Square
from game_functionality.move import Move


class SinglePlay:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hexapawn")
        self.game = Game()

    def player_turn(self, event):
        dragger = self.game.dragger
        board = self.game.board
        game = self.game
        screen = self.screen

        if event.type == pygame.MOUSEBUTTONDOWN and not board.winner:
            dragger.update_mouse(event.pos)

            clicked_row = dragger.mouseY // SQSIZE
            clicked_col = dragger.mouseX // SQSIZE

            # If square has piece
            if board.squares[clicked_row][clicked_col].has_piece():
                piece = board.squares[clicked_row][clicked_col].piece
                # valid piece color
                if piece.color == game.next_player:

                    board.calc_moves(
                        piece, clicked_row, clicked_col)
                    dragger.save_initial(event.pos)
                    dragger.drag_piece(piece)

                    # show methods
                    game.show_bg(screen)
                    game.show_last_move(screen)
                    game.show_moves(screen)
                    game.show_pieces(screen)

        elif event.type == pygame.MOUSEMOTION and not board.winner:

            motion_row = event.pos[1] // SQSIZE
            motion_col = event.pos[0] // SQSIZE

            game.set_hover(motion_row, motion_col)

            if dragger.dragging:
                dragger.update_mouse(event.pos)

                # show methods
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)

                game.show_pieces(screen)
                game.show_hover(screen)
                dragger.update_blit(screen)

        elif event.type == pygame.MOUSEBUTTONUP and not board.winner:

            if dragger.dragging:
                dragger.update_mouse(event.pos)

                released_row = dragger.mouseY // SQSIZE
                released_col = dragger.mouseX // SQSIZE

                # create possible move
                initial = Square(dragger.initial_row,
                                    dragger.initial_col)
                final = Square(released_row, released_col)
                move = Move(initial, final)

                # valid move ?
                if board.valid_moves(dragger.piece, move):
                    captured = board.squares[released_row][released_col].has_piece(
                    )
    
                    board.move(dragger.piece, move)
                    # show methods
                    game.show_bg(screen)
                    game.show_last_move(screen)
                    game.show_pieces(screen)
                    

                    # check if game is over
                    board.check_winner(game.next_player)

                    game.next_turn()

                dragger.undrag_piece()


    def mainloop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board
        ai = self.game.ai

        while True:
            if board.winner:
                game.show_winner(screen, board.winner)
            else:
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                if game.next_player == "white":
                    if not board.winner:
                        self.player_turn(event)

                else:   # AI turn
                    if not board.winner:
                        move = ai.get_move(board)
                        board.move(move.piece, move)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_pieces(screen)
                        game.next_turn()
                        board.check_winner()


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset()
                        screen = self.screen
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                if event.type == pygame.QUIT:
                    sys.exit()

            pygame.display.update()


        
        