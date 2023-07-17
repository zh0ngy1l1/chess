import pygame
import os
import copy

def fen_to_current_position(fen):
    current_position = [[None] * 8 for _ in range(8)]
    fen_parts = fen.split(" ")

    # Process the piece positions part of the FEN string
    fen_pieces = reversed(fen_parts[0])
    rank_index = 7
    file_index = 0

    for char in fen_pieces:
        if char == '/':
            rank_index -= 1
            file_index = 0
        elif char.isdigit():
            file_index += int(char)
        else:
            current_position[rank_index][file_index] = "b" + char if char.islower() else "w" + char.lower()
            file_index += 1

    return current_position


class Chessboard:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Define the colors
        self.BLACK = (100, 100, 150)
        self.WHITE = (255, 255, 255)
        self.GREY = (128, 128, 128)

        # White's turn
        self.turn = "w"

        #TODO REMOVE KING's ABILITY TO CASTLE


        # Hands
        self.bughouse_hand_amounts = [[1, 0, 0, 0, 0],[0, 1, 1, 0, 0]]
        self.bughouse_hand_names = ["q", "r", "n", "b", "p"]

        # Set the size of each square on the chessboard
        self.square_size = 64
        self.board_width = 8 * self.square_size
        self.board_height = 12 * self.square_size

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
        fen = "2qrr1k1/pb3ppp/1p2n3/1N1p4/4n3/BP1QPB1n/P4PPP/3R1RK1 w - - 6 21"
        self.current_position = fen_to_current_position(starting_fen)
        self.current_position = fen_to_current_position(fen)

        # Initialize the piece objects with their locations
        self.all_pieces = []
        for row in range(8):
            for column in range(8):
                piece_name = self.current_position[row][column]
                if piece_name:
                    piece = Piece(piece_name[0], piece_name[-1], row, column)
                    self.current_position[row][column] = piece
                    self.all_pieces.append(piece)

    def draw_chessboard(self):
        for row in [0, 11]:
            for column in range(1, 6):
                x = column * self.square_size
                y = row * self.square_size

                # Toggle the square color
                if (row + column) % 2 == 0:
                    color = self.WHITE
                else:
                    color = self.BLACK
         
                # Draw the square
                pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))

                piece_name = self.bughouse_hand_names[column - 1]

                if row:
                    piece_image = self.piece_images["w" + piece_name]
                    piece_amount = self.bughouse_hand_amounts[1][column - 1]
                
                else:
                    piece_image = self.piece_images["b" + piece_name]
                    piece_amount = self.bughouse_hand_amounts[0][column - 1]

                self.screen.blit(piece_image, (x, y))
                font = pygame.font.Font(None, 24)
                text = font.render(str(piece_amount), True, (255, 0, 0))
                text_rect = text.get_rect(center=(x + self.square_size * 3 // 4, y + self.square_size * 3 // 4))
                self.screen.blit(text, text_rect)

        # Loop to draw the chessboard and pieces
        for row in range(8):
            for column in range(8):
                x = column * self.square_size
                y = (row + 2) * self.square_size # offset for bughouse hand

                # Toggle the square color
                if (row + column) % 2 == 0:
                    color = self.WHITE
                else:
                    color = self.BLACK

                # Draw the square
                pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))

                # Get the piece name at the current position
                piece = self.current_position[row][column]

                # If a piece is present, blit the corresponding image
                if piece:
                    piece_image = self.piece_images[piece.color + piece.piece_name]
                    self.screen.blit(piece_image, (x, y))

    def display_legal_moves(self, moves):
        # Loop to display the legal moves as grey circles on the chessboard
        for move in moves:
            row, column = move
            x = column * self.square_size + self.square_size // 2
            y = (row + 2) * self.square_size + self.square_size // 2
            radius = 12
            pygame.draw.circle(self.screen, self.GREY, (x, y), radius)

    def run_game_loop(self):
        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_position = pygame.mouse.get_pos()
                        row = mouse_position[1] // self.square_size
                        column = mouse_position[0] // self.square_size

                        # Remove dots indicating legal moves
                        self.draw_chessboard()

                        if 2 <= row <= 9:
                            # Get the piece object at the clicked position
                            piece = self.current_position[row - 2][column] # bughouse offset
                            # Check if a piece is clicked
                            if piece:
                                if piece.color == self.turn:
                                    legal_moves = piece.show_legal_moves(self.current_position, self.all_pieces)
                                    self.display_legal_moves(legal_moves)
                                    print(legal_moves)
                        
                        elif 1 <= column <=5:
                            if self.turn == "w" and row == 11:
                                print(self.bughouse_hand_names[column - 1], self.bughouse_hand_amounts[1][column - 1])
                            elif self.turn == "b" and row == 0:
                                print(self.bughouse_hand_names[column - 1], self.bughouse_hand_amounts[0][column - 1])
                            

                        


            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()


class Piece:
    def __init__(self, color, piece_name, row, column):
        self.piece_name = piece_name
        self.color = color
        self.location = (row, column)
        self.can_castle = True if piece_name == "k" else False

    def show_legal_moves(self, current_position, strict=True):
        # Implement the logic to show legal moves for the piece
        moves = []

        # Get the current position of the piece
        current_row, current_column = self.location

        # Bishop moves
        if self.piece_name == "b":
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                for i in range(1, 8):
                    new_row = current_row + i * dx
                    new_column = current_column + i * dy
                    if 0 <= new_row < 8 and 0 <= new_column < 8:
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
                    if 0 <= new_row < 8 and 0 <= new_column < 8:
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
                    if 0 <= new_row < 8 and 0 <= new_column < 8:
                        if current_position[new_row][new_column] is None:
                            moves.append((new_row, new_column))
                        elif current_position[new_row][new_column].color != self.color:
                            moves.append((new_row, new_column))

        # Queen moves
        elif self.piece_name == "q":
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                for i in range(1, 8):
                    new_row = current_row + i * dx
                    new_column = current_column + i * dy
                    if 0 <= new_row < 8 and 0 <= new_column < 8:
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
            knight_moves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
            for dx, dy in knight_moves:
                new_row = current_row + dx
                new_column = current_column + dy
                if 0 <= new_row < 8 and 0 <= new_column < 8:
                    if current_position[new_row][new_column] is None or current_position[new_row][new_column].color != self.color:
                        moves.append((new_row, new_column))

        # Pawn moves
        elif self.piece_name == "p":
            if self.color == "w":
                # Moves for white pawn
                new_row = current_row - 1
                if 0 <= new_row < 8:
                    if current_position[new_row][current_column] is None:
                        moves.append((new_row, current_column))

                    if current_row == 6 and current_position[new_row][current_column] is None and current_position[new_row-1][current_column] is None:
                        moves.append((new_row-1, current_column))

                # Capturing moves
                capture_moves = [(current_row - 1, current_column - 1), (current_row - 1, current_column + 1)]
                for move in capture_moves:
                    new_row, new_column = move
                    if 0 <= new_row < 8 and 0 <= new_column < 8:
                        if current_position[new_row][new_column] is not None and current_position[new_row][new_column].color != self.color:
                            moves.append(move)

            else:
                # Moves for black pawn
                new_row = current_row + 1
                if 0 <= new_row < 8:
                    if current_position[new_row][current_column] is None:
                        moves.append((new_row, current_column))

                    if current_row == 1 and current_position[new_row][current_column] is None and current_position[new_row+1][current_column] is None:
                        moves.append((new_row+1, current_column))

                # Capturing moves
                capture_moves = [(current_row + 1, current_column - 1), (current_row + 1, current_column + 1)]
                for move in capture_moves:
                    new_row, new_column = move
                    if 0 <= new_row < 8 and 0 <= new_column < 8:
                        if current_position[new_row][new_column] is not None and current_position[new_row][new_column].color != self.color:
                            moves.append(move)
        
        illegal_moves = []
        
        if strict:
            # test if move is illegal because king can be captured
            
            for move in moves:


                #make new move location
                new_row, new_column = move

                temp_position = copy.deepcopy(current_position)
                temp_piece = temp_position[current_row][current_column]
                temp_piece.location = (new_row, new_column)
                temp_position[new_row][new_column] = temp_piece
                temp_position[current_row][current_column] = None
                #create new temporary position, with the possibly illegal move played

                temp_all_pieces = []
                for row in temp_position:
                    temp_all_pieces.extend([piece for piece in row if piece != None])

                # find king
                for some_piece in temp_all_pieces:
                    if some_piece.piece_name == "k" and some_piece.color == self.color:
                        king_location = some_piece.location
                        print("king at", king_location)

                for enemy_piece in temp_all_pieces:
                    if enemy_piece.color != self.color and enemy_piece.location != self.location:
                        if king_location in enemy_piece.show_legal_moves(temp_position, strict=False):
                            illegal_moves.append(move)

        return [move for move in moves if move not in illegal_moves]


# Create an instance of the Chessboard class
chessboard = Chessboard()

# Draw the chessboard and pieces
chessboard.draw_chessboard()

# Run the game loop
chessboard.run_game_loop()
