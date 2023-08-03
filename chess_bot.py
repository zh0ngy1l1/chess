import pygame
import os
import copy


class Chessboard:
    def fen_to_current_position(self, fen):
        """
        from given fen string create self.current_position as a 2d-list with piece objects.
        """

        self.current_position = [[None] * 8 for _ in range(8)]
        fen_parts = fen.split(" ")

        # Process the piece positions part of the FEN string
        fen_pieces = fen_parts[0]
        rank_index = 0
        file_index = 0

        # logic
        for char in fen_pieces:
            if char == "/":
                rank_index += 1
                file_index = 0
            elif char.isdigit():
                file_index += int(char)
            else:
                self.current_position[rank_index][file_index] = Piece(
                    "b" if char.islower() else "w", char.lower(), rank_index, file_index
                )
                file_index += 1

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Define the colors and font
        self.BLACK = (0, 0, 0)
        self.BLUE = (100, 100, 150)
        self.WHITE = (255, 255, 255)
        self.GREY = (128, 128, 128)
        self.RED = (150, 100, 100)
        self.font = pygame.font.Font(None, 24)

        # White's turn
        self.turn = "w"
        self.selected_piece = None
        self.previous_move = []
        self.about_to_promote = False

        # Names of pieces in promotion menu
        self.promotion_menu_names = ["q", "r", "n", "b", "p"]

        # Set the size of each square on the chessboard
        self.square_size = 64
        self.board_width = 8 * self.square_size
        self.board_height = 8 * self.square_size

        # Create the Pygame screen
        self.screen = pygame.display.set_mode((self.board_width, self.board_height))

        # Set the window title
        pygame.display.set_caption("Chessboard")

        # Load the piece images
        self.piece_images = {}

        # Path to the directory containing the PNG images
        directory = "icons"

        # Get a list of files in the directory
        files = os.listdir(directory)

        # Loop through the files
        for file in files:
            # Check if the file is a PNG
            if file.endswith(".png"):
                # Remove the file extension to get the piece name
                piece_name = os.path.splitext(file)[0]

                # Load the image using Pygame
                image_path = os.path.join(directory, file)
                image = pygame.image.load(image_path)

                # Add the image to the dictionary
                self.piece_images[piece_name] = image

        # Define the starting positions for the pieces
        starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        fen = "rnbqkbnr/pppppppp/8/8/8/4n3/PPPPPPPP/R3K2Q"
        self.fen_to_current_position(starting_fen)
        
    def draw_chessboard(self):
        """
        update board to match position
        """

        # Paint screen background
        pygame.draw.rect(
            self.screen, self.BLACK, (0, 0, self.board_width, self.board_height)
        )

        # Loop to draw the chessboard and pieces
        for row in range(8):
            for column in range(8):
                x = column * self.square_size
                y = row * self.square_size

                # Toggle the square color
                if (row, column) in self.previous_move:
                    color = self.RED
                elif (row + column) % 2 == 0:
                    color = self.WHITE
                else:
                    color = self.BLUE

                # Draw the square
                pygame.draw.rect(
                    self.screen, color, (x, y, self.square_size, self.square_size)
                )

                # Get the piece name at the current position
                piece = self.current_position[row][column]

                # If a piece is present, draw the corresponding image
                if piece:
                    piece_image = self.piece_images[piece.color + piece.piece_name]
                    self.screen.blit(piece_image, (x, y))

    def draw_promotion_menu(self):
        """
        draw menu for promotion.
        """

        # Row 1 for white
        if self.turn == "w":
            y = 1 * self.square_size

        # Row 6 for black
        else:
            y = 6 * self.square_size

        # Draw the menu, square by square
        for column in range(2, 6):
            x = column * self.square_size

            # Draw the background square
            pygame.draw.rect(
                self.screen, self.WHITE, (x, y, self.square_size, self.square_size)
            )
            pygame.draw.rect(
                self.screen,
                self.GREY,
                (x, y, self.square_size, self.square_size),
                width=4,
            )

            # Draw the piece
            piece_name = self.promotion_menu_names[column - 2]
            piece_image = self.piece_images[self.turn + piece_name]
            self.screen.blit(piece_image, (x, y))

    def display_legal_moves(self, moves):
        """
        Display the legal moves as grey circles on the chessboard
        """
        for move in moves:
            row, column = move
            x = column * self.square_size + self.square_size // 2
            y = row * self.square_size + self.square_size // 2
            if self.current_position[row][column] is not None:  # if capturing
                pygame.draw.circle(self.screen, self.GREY, (x, y), radius=20, width=4)
            else:
                pygame.draw.circle(self.screen, self.GREY, (x, y), radius=12)

    def detect_checkmate(self):
        all_pieces = []
        for row in self.current_position:
            all_pieces.extend([piece for piece in row if piece != None])

        # find king
        for some_piece in all_pieces:
            if some_piece.piece_name == "k" and some_piece.color == self.turn:
                king_row, king_column = some_piece.location

        king = self.current_position[king_row][king_column]
        moves = king.show_legal_moves(self.current_position, strict=True)
        
        # Checkmate detection
        if len(moves) == 0:
            print("king can't move")
            temp_position = copy.deepcopy(self.current_position)

            #create temporary own pieces and enemy pieces lists
            temp_own_pieces = []
            temp_enemy_pieces = []
            for row in temp_position:
                for some_piece in row:
                    if some_piece != None:
                        if some_piece.color == self.turn:
                            temp_own_pieces.append(some_piece)
                        else:
                            temp_enemy_pieces.append(some_piece)
                    else:
                        pass
            

            # find all legal moves
            all_moves = []
            for some_piece in temp_own_pieces:
                some_piece_moves = some_piece.show_legal_moves(
                    temp_position, self.previous_move, strict=True
                )
                print(some_piece.piece_name, some_piece_moves)
                all_moves.extend(some_piece_moves)

            if len(all_moves) == 0:
                checkmate = False

                # detect checkmate
                for enemy_piece in temp_enemy_pieces:
                    if (
                        enemy_piece.color != self.turn
                    ):
                        if (king_row, king_column) in enemy_piece.show_legal_moves(
                            temp_position, None, strict=False
                        ):
                            checkmate = True

                if checkmate:            
                    print(f"CHECKMATE! {'WHITE' if self.turn == 'b' else 'BLACK'} WINS!")
                else:
                    print("STALEMATE! IT'S A DRAW!")


    def make_move(self, target_location, en_passant=False, promotion=False):
        """
        make the move.
        change the previous move.
        change the turn
        """

        print(f"moving {self.selected_piece.piece_name} from {self.selected_piece.location} to {target_location}")

        target_row, target_column = target_location

        original_row, original_column = self.selected_piece.location


        self.previous_move = [
            self.selected_piece.piece_name,
            (original_row, original_column),
            (target_row, target_column),
        ]
        
        self.current_position[original_row][original_column] = None

        # castling
        if self.selected_piece.piece_name == "k" and \
            (target_column - original_column > 1 or target_column - original_column < - 1):
                # get castled rook
                rook_column, rook_target_column = (0, 3) if target_column == 2 else (7, 5)

                self.previous_move = [
                    self.selected_piece.piece_name,
                    (original_row, original_column),
                    (original_row, target_column),
                    (original_row, rook_column),
                    (original_row, rook_target_column)
                ]

                rook = self.current_position[original_row][rook_column]
                self.current_position[original_row][rook_column] = None

                self.current_position[original_row][rook_target_column] = rook
                rook.location = (target_row, rook_target_column)

                self.current_position[target_row][target_column] = self.selected_piece
                self.selected_piece.location = (target_row, target_column)

                self.selected_piece.has_moved = True
                rook.has_moved = True

        else:
            if promotion:
                self.current_position[target_row][target_column] = Piece(
                    self.turn, promotion, target_row, target_column
                )
                self.selected_piece.location = (target_row, target_column)
                self.selected_piece.has_moved = True

            # normal move
            else:
                self.current_position[target_row][target_column] = self.selected_piece
                self.selected_piece.location = (target_row, target_column)
                self.selected_piece.has_moved = True

                if en_passant:
                    self.current_position[original_row][target_column] = None

        self.turn = "w" if self.turn == "b" else "b"
        self.detect_checkmate()
        self.selected_piece = None

    def run_game_loop(self):
        """
        main game loop. no arguments, no return,  just call this.
        """
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_position = pygame.mouse.get_pos()
                        row = mouse_position[1] // self.square_size
                        column = mouse_position[0] // self.square_size

                        # Remove dots indicating legal moves
                        self.draw_chessboard()

                        # Promotion
                        menu_row, promotion_row = (
                            (1, 0) if self.turn == "w" else (6, 7)
                        )

                        if self.about_to_promote:
                            if row == menu_row and 2 <= column <= 5:
                                # use previous row/column and promote
                                self.make_move(
                                    self.previous_move[-1],
                                    promotion=self.promotion_menu_names[column - 2],
                                )
                                self.draw_chessboard()
                                self.about_to_promote = False
                            else:
                                self.draw_promotion_menu()


                        # Get the piece object at the clicked position
                        piece = self.current_position[row][column]

                        # Check if a piece is clicked
                        if piece:
                            # Select own piece
                            if piece.color == self.turn:
                                legal_moves = piece.show_legal_moves(
                                    self.current_position,
                                    self.previous_move,
                                    strict=True,
                                )
                                self.display_legal_moves(legal_moves)
                                print(
                                    f"selected piece {piece.piece_name} at {piece.location} with legal moves {legal_moves}"
                                )

                                self.selected_piece = piece

                            # Capture enemy piece
                            elif self.selected_piece is not None:
                                if (
                                    row,
                                    column,
                                ) in legal_moves:
                                    # Promotion
                                    if (
                                        self.selected_piece.piece_name == "p"
                                        and row == promotion_row
                                    ):
                                        print(
                                            f"promotion. {self.selected_piece.piece_name} at {self.selected_piece.location} captures {piece.piece_name} on {row, column} and promotes."
                                        )
                                        self.draw_promotion_menu()
                                        self.about_to_promote = True
                                        self.previous_move = [self.selected_piece.piece_name, (self.selected_piece.location), (row, column)]

                                    else:
                                        print(
                                            f"play move. {self.selected_piece.piece_name} at {self.selected_piece.location} captures {piece.piece_name} on {row, column}."
                                        )

                                        # Play the move on the board
                                        self.make_move(
                                            (row, column)
                                        )
                                        self.draw_chessboard()

                        # Move own piece
                        elif self.selected_piece is not None:
                            if (row, column) in legal_moves:
                                # En passant
                                if (
                                    self.selected_piece.piece_name == "p"
                                    and row != self.selected_piece.location[0]
                                    and column != self.selected_piece.location[1]
                                ):
                                    print(
                                        f"en passant. {self.selected_piece.piece_name} at {self.selected_piece.location} moves to {(row, column)}."
                                    )

                                    self.make_move(
                                        (row, column),
                                        en_passant=True,
                                    )

                                    self.draw_chessboard()

                                # Promotion
                                elif (
                                    self.selected_piece.piece_name == "p"
                                    and row == promotion_row
                                ):
                                    print(
                                        f"promotion. {self.selected_piece.piece_name} at {self.selected_piece.location} promotes."
                                    )
                                    self.draw_promotion_menu()
                                    self.about_to_promote = True
                                    self.previous_move = [self.selected_piece.piece_name, (self.selected_piece.location), (row, column)]

                                else:
                                    print(
                                        f"play move. {self.selected_piece.piece_name} at {self.selected_piece.location} moves to {(row, column)}."
                                    )

                                    # Play the move on the board
                                    self.make_move(
                                        (row, column)
                                    )
                                    self.draw_chessboard()
                            else:
                                self.selected_piece = None

                        else:
                            self.selected_piece = None


            # Update the display
            pygame.display.flip()
            

        # Quit Pygame
        pygame.quit()



class Piece:
    def __init__(self, color, piece_name, row, column):
        # Initialize values
        self.piece_name = piece_name
        self.color = color
        self.location = (row, column)
        self.has_moved = False

    def show_legal_moves(self, current_position, previous_move=None, strict=False):
        """
        return all legal moves for the piece as (row, col)
        """
        moves = []

        # Get the current position of the piece
        current_row, current_column = self.location

        # Bishop moves
        if self.piece_name == "b":
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                for i in range(1, 8):
                    new_row = current_row + i * dx
                    new_column = current_column + i * dy
                    if 0 <= new_row <= 7 and 0 <= new_column <= 7:
                        if current_position[new_row][new_column] is None:
                            moves.append((new_row, new_column))
                        elif current_position[new_row][new_column].color != self.color:
                            moves.append((new_row, new_column))
                            break
                        else:
                            break
                    else:
                        break

        # Rook moves
        elif self.piece_name == "r":
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                for i in range(1, 8):
                    new_row = current_row + i * dx
                    new_column = current_column + i * dy
                    if 0 <= new_row <= 7 and 0 <= new_column <= 7:
                        if current_position[new_row][new_column] is None:
                            moves.append((new_row, new_column))
                        elif current_position[new_row][new_column].color != self.color:
                            moves.append((new_row, new_column))
                            break
                        else:
                            break
                    else:
                        break

        # King moves
        elif self.piece_name == "k":
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    new_row = current_row + dx
                    new_column = current_column + dy
                    if 0 <= new_row <= 7 and 0 <= new_column <= 7:
                        if current_position[new_row][new_column] is None:
                            moves.append((new_row, new_column))
                        elif current_position[new_row][new_column].color != self.color:
                            moves.append((new_row, new_column))

            # Castling.
            if self.has_moved == False and strict:
                for dy, rook_column in [(-2, 0), (2, 7)]:
                    if (
                        current_position[current_row][current_column + dy] is None
                        and current_position[current_row][current_column + dy // 2]
                        is None
                    ):
                        rook = current_position[current_row][rook_column]
                        if rook is None:
                            continue
                        else:
                            if (
                                rook.piece_name == "r"
                                and rook.color == self.color
                                and rook.has_moved == False
                            ):
                                # Test if king under check

                                all_pieces = []
                                for row in current_position:
                                    all_pieces.extend(
                                        [piece for piece in row if piece != None]
                                    )

                                under_check = False
                                for enemy_piece in all_pieces:
                                    if enemy_piece.color != self.color:
                                        if (
                                            self.location
                                            in enemy_piece.show_legal_moves(
                                                current_position, None, strict=False
                                            )
                                        ):
                                            print(
                                                f"under check by {enemy_piece.piece_name} at {enemy_piece.location}"
                                            )
                                            under_check = True

                                # Test if castling through check
                                new_column = current_column + dy // 2

                                king_location = (current_row, new_column)

                                castling_through_check = False
                                for enemy_piece in all_pieces:
                                    if enemy_piece.color != self.color:
                                        if (
                                            king_location
                                            in enemy_piece.show_legal_moves(
                                                current_position, None, strict=False
                                            )
                                        ):
                                            print(
                                                f"trying to castle through check by {enemy_piece.piece_name} at {enemy_piece.location}"
                                            )
                                            castling_through_check = True

                                if not castling_through_check and not under_check:
                                    new_column = current_column + dy
                                    moves.append((current_row, new_column))

        # Queen moves
        elif self.piece_name == "q":
            for dx, dy in [
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
            ]:
                for i in range(1, 8):
                    new_row = current_row + i * dx
                    new_column = current_column + i * dy
                    if 0 <= new_row <= 7 and 0 <= new_column <= 7:
                        if current_position[new_row][new_column] is None:
                            moves.append((new_row, new_column))
                        elif current_position[new_row][new_column].color != self.color:
                            moves.append((new_row, new_column))
                            break
                        else:
                            break
                    else:
                        break

        # Knight moves
        elif self.piece_name == "n":
            knight_moves = [
                (1, 2),
                (1, -2),
                (-1, 2),
                (-1, -2),
                (2, 1),
                (2, -1),
                (-2, 1),
                (-2, -1),
            ]
            for dx, dy in knight_moves:
                new_row = current_row + dx
                new_column = current_column + dy
                if 0 <= new_row <= 7 and 0 <= new_column <= 7:
                    if (
                        current_position[new_row][new_column] is None
                        or current_position[new_row][new_column].color != self.color
                    ):
                        moves.append((new_row, new_column))

        # Pawn moves
        elif self.piece_name == "p":
            if self.color == "w":
                # Moves for white pawn
                new_row = current_row - 1
                if 0 <= new_row <= 7:
                    if current_position[new_row][current_column] is None:
                        moves.append((new_row, current_column))

                    if (
                        current_row == 6
                        and current_position[new_row][current_column] is None
                        and current_position[new_row - 1][current_column] is None
                    ):
                        moves.append((new_row - 1, current_column))

                # Capturing moves
                capture_moves = [
                    (current_row - 1, current_column - 1),
                    (current_row - 1, current_column + 1),
                ]
                for move in capture_moves:
                    new_row, new_column = move
                    if 0 <= new_row <= 7 and 0 <= new_column <= 7:
                        if (
                            current_position[new_row][new_column] is not None
                            and current_position[new_row][new_column].color
                            != self.color
                        ):
                            moves.append(move)

                # En passant
                if current_row == 3:
                    for enemy_column in [current_column - 1, current_column + 1]:
                        if previous_move == ["p", (1, enemy_column), (3, enemy_column)]:
                            moves.append((new_row, enemy_column))

            else:
                # Moves for black pawn
                new_row = current_row + 1
                if 0 <= new_row <= 7:
                    if current_position[new_row][current_column] is None:
                        moves.append((new_row, current_column))

                    if (
                        current_row == 1
                        and current_position[new_row][current_column] is None
                        and current_position[new_row + 1][current_column] is None
                    ):
                        moves.append((new_row + 1, current_column))

                # Capturing moves
                capture_moves = [
                    (current_row + 1, current_column - 1),
                    (current_row + 1, current_column + 1),
                ]
                for move in capture_moves:
                    new_row, new_column = move
                    if 0 <= new_row <= 7 and 0 <= new_column <= 7:
                        if (
                            current_position[new_row][new_column] is not None
                            and current_position[new_row][new_column].color
                            != self.color
                        ):
                            moves.append(move)

                # En passant
                if current_row == 4:
                    for enemy_column in [current_column - 1, current_column + 1]:
                        if previous_move == ["p", (6, enemy_column), (4, enemy_column)]:
                            moves.append((new_row, enemy_column))

        illegal_moves = []

        # test if move is illegal because king can be captured
        if strict:
            for move in moves:
                # make new move location
                new_row, new_column = move

                temp_position = copy.deepcopy(current_position)
                temp_piece = temp_position[current_row][current_column]
                temp_piece.location = (new_row, new_column)
                temp_position[new_row][new_column] = temp_piece
                temp_position[current_row][current_column] = None
                # create new temporary position, with the possibly illegal move played

                temp_all_pieces = []
                for row in temp_position:
                    temp_all_pieces.extend([piece for piece in row if piece != None])

                # find king
                for some_piece in temp_all_pieces:
                    if some_piece.piece_name == "k" and some_piece.color == self.color:
                        king_location = some_piece.location

                for enemy_piece in temp_all_pieces:
                    if (
                        enemy_piece.color != self.color
                        and enemy_piece.location != self.location
                    ):
                        if king_location in enemy_piece.show_legal_moves(
                            temp_position, None, strict=False
                        ):
                            illegal_moves.append(move)

        moves = [move for move in moves if move not in illegal_moves]
        return moves

# Create an instance of the Chessboard class
chessboard = Chessboard()

# Draw the chessboard and pieces
chessboard.draw_chessboard()

# Run the game loop
chessboard.run_game_loop()
