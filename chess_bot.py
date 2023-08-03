import copy
from chess import Chessboard

class Chessbot:
    def __init__(self):
        self.fen = "rnbqkbnr/ppppp2p/8/8/8/8/PPPP1PPP/RNBQKBNR"
        self.original_chessboard = Chessboard(self.fen)
        

    def find_mateinone(self):

        # create temporary own pieces and enemy pieces lists
        own_pieces = []
        enemy_pieces = []
        for row in self.original_chessboard.current_position:
            for some_piece in row:
                if some_piece != None:
                    if some_piece.color == self.original_chessboard.turn:
                        own_pieces.append(some_piece)
                    else:
                        enemy_pieces.append(some_piece)
                else:
                    pass
        
        all_moves = []
        # find all legal moves for each piece
        for some_piece in own_pieces:
            self.original_chessboard.selected_piece = some_piece

            some_piece_moves = some_piece.show_legal_moves(
                self.original_chessboard.current_position, self.original_chessboard.previous_move, strict=True
            )

            print(some_piece.piece_name, some_piece_moves)
            all_moves.extend([(some_piece, move) for move in some_piece_moves])
        
        for move in all_moves:
            temporary_chessboard = Chessboard(self.f)
            temporary_chessboard.selected_piece = move[0]
            temporary_chessboard.make_move(move[1])
            temporary_chessboard.detect_checkmate()

bot = Chessbot()
bot.find_mateinone()