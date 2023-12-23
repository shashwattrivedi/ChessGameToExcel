from numpy import genfromtxt, positive, right_shift
import numpy as np
import os

class ChessBoardCsvCreater:
    def __init__(self, pieces_dir, game_dir):
        self.pieces_values_dict = dict()
        self.game_dir = game_dir

        for filename in os.listdir(pieces_dir):
            if filename.endswith(".csv"): 
                piece = str(filename.split(".csv")[0])
                self.pieces_values_dict[piece] = genfromtxt(os.path.join(pieces_dir, filename), delimiter=',', dtype=int)
            else:
                continue
        
        assert len(self.pieces_values_dict) == 26

        self.chess_board = [['BRW','BNB','BBW','BQB','BKW','BBB','BNW','BRB'],
                            ['BPB','BPW','BPB','BPW','BPB','BPW','BPB','BPW'],
                            ['W','B','W','B','W','B','W','B'],
                            ['B','W','B','W','B','W','B','W'],
                            ['W','B','W','B','W','B','W','B'],
                            ['B','W','B','W','B','W','B','W'],
                            ['WPW','WPB','WPW','WPB','WPW','WPB','WPW','WPB'],
                            ['WRB','WNW','WBB','WQW','WKB','WBW','WNB','WRW']]

        # print(self.pieces_values_dict['W'].shape)
        self.dim_x = self.pieces_values_dict['W'].shape[0]
        self.dim_y = self.pieces_values_dict['W'].shape[1]
        self.chess_squares = 8

        self.initial_WK_rank = self.chess_squares - 1
        self.initial_WK_file = 4

        self.initial_BK_rank = 0
        self.initial_BK_file = 4      

    def render(self):
        chess_board_rendered = [[0] * self.dim_x * self.chess_squares] * self.chess_squares * self.dim_y
        chess_board_rendered = np.array(chess_board_rendered)

        for rank, row in enumerate(self.chess_board):
            for file, piece in enumerate(row):
                chess_board_rendered[rank * self.dim_x : (rank + 1) * self.dim_x , file * self.dim_y : (file + 1) * self.dim_y] = self.pieces_values_dict[piece]

        return chess_board_rendered

    def create_chess_board_csv(self, move_number, player):
        np.savetxt(self.game_dir + "\\" + str(move_number) + player + '.csv', self.render(), delimiter=",")

    def get_move(self, move, player):
        move_len = len(move)
        capture = False
        valid_positions = None

        initial_rank = None
        initial_file = None

        final_rank = self.chess_squares - int(move[move_len - 1])
        final_file = ord(move[move_len - 2]) - ord('a')

        if (move_len == 2 or (move[0] in ['a','b','c','d','e','f','g','h'])):
            piece = 'P'

            if (move_len == 3 or 'x' in move):
                capture = True
                initial_file = ord(move[0]) - ord('a')

        else:
            if ('x' in move):
                capture = True
            
            piece = move[0]

            final_loc_start =  move_len - 3  if capture else move_len - 2

            if (final_loc_start == 2):
                if (move[1] in ['a','b','c','d','e','f','g','h']):
                    initial_file = ord(move[1]) - ord('a')
                else:
                    initial_file = int(move[1]) - 1

            if (final_loc_start == 3):
                initial_file = ord(move[1]) - ord('a')
                initial_rank = self.chess_squares - int(move[2])

        if (piece == 'P' and capture):
            valid_positions = self.search_location_pawn_capture(final_rank, final_file, player)

        if (piece == 'P' and not capture):
            valid_positions = self.search_location_pawn(final_rank, final_file, player)

        if (piece == 'B'):
            valid_positions = self.search_location_bishop(final_rank, final_file)

        if (piece == 'Q'):
            valid_positions = self.search_location_queen(final_rank, final_file)

        if (piece == 'N'):
            valid_positions = self.search_location_knight(final_rank, final_file)

        if (piece == 'R'):
            valid_positions = self.search_location_rook(final_rank, final_file)

        if (piece == 'K'):
            valid_positions = self.search_location_king(final_rank, final_file)

        if (valid_positions == None or len(valid_positions) == 0):
            raise Exception("Invalid Move " + move)

        else:

            invalid_positions = []
            if (initial_rank != None):
                    for position in valid_positions:
                        if (position[0] != initial_rank):
                            invalid_positions.append(position)

            if (initial_file != None):
                for position in valid_positions:
                    if (position[1] != initial_file):
                        invalid_positions.append(position)

            valid_positions = list(set(valid_positions) - set(invalid_positions))

            _valid_positions = []                
            for position in valid_positions:
                if (self.chess_board[position[0]][position[1]].startswith(player + piece)):
                    _valid_positions.append(position)

            valid_positions = _valid_positions

            invalid_positions = []
            for position in valid_positions:
                if not (self.is_piece_move_valid( (position,(final_rank, final_file)), piece, move)):
                    invalid_positions.append(position)

            valid_positions = list(set(valid_positions) - set(invalid_positions))

            if (len(valid_positions) != 1):
                # for position in valid_positions:
                    # print(position)                   
                raise Exception("Invalid move " + move)

            return (valid_positions[0] , (final_rank, final_file))

    def is_piece_move_valid(self, simplified_move, piece, move):

        if (piece == 'R' or piece == 'Q'):
            if (simplified_move[0][0] == simplified_move[1][0]):
                start = min(simplified_move[0][1], simplified_move[1][1])
                end = max(simplified_move[0][1], simplified_move[1][1])

                for file in range(start + 1, end):
                    if not self.chess_board[simplified_move[0][0]][file] in ['B', 'W']:
                        return False
                
                return True

            else:
                if (simplified_move[0][1] == simplified_move[1][1]):
                    start = min(simplified_move[1][0], simplified_move[1][0])
                    end = max(simplified_move[1][0], simplified_move[1][0])

                    for rank in range(start + 1, end):
                        if not self.chess_board[rank][simplified_move[0][0]] in ['B', 'W']:
                            return False

                return True             

        if (piece == 'B' or piece == 'Q'):
            leftmost_file, rightmost_file = (simplified_move[0], simplified_move[1]) if simplified_move[0][1] < simplified_move[1][1] else (simplified_move[1], simplified_move[0])

            # print ( leftmost_file)
            # print(rightmost_file)
            slope = (rightmost_file[1] -  leftmost_file[1]) / (rightmost_file[0] -  leftmost_file[0])

            if not (slope == 1.0 or slope == -1.0):
                raise Exception("Invalid move " + move)
            
            slope = int(slope)
            search_loc = leftmost_file[0] + slope , leftmost_file[1] + abs(slope)
            while (search_loc[0] != rightmost_file[0] and search_loc[1] != rightmost_file[1]):
                # print("Searching " + str(search_loc[0]) + " " + str(search_loc[1]))
                if not self.chess_board[search_loc[0]][search_loc[1]] in ['B', 'W']:
                    return False

                search_loc = search_loc[0] + slope , search_loc[1] + abs(slope)

            return True

        if (piece == 'P'):
            if ( 'x' in move or len(move) > 2):
                return True
            
            else:
                for rank in range(simplified_move[1][0], simplified_move[1][0]):
                    if not self.chess_board[rank][simplified_move[0][1]] in ['B', 'W']:
                        return False
            
            return True
            
        if (piece == 'N' or piece == 'K'):
            return True

        return False

    def execute_move(self, move, player):

        if (move == 'O-O' and player == 'W'):

            self.chess_board[self.initial_WK_rank][self.initial_WK_file] = 'B'
            self.chess_board[self.initial_WK_rank][self.initial_WK_file + 2] = 'WKB'

            self.chess_board[self.initial_WK_rank][self.initial_WK_file + 3] = 'W'
            self.chess_board[self.initial_WK_rank][self.initial_WK_file + 1] = 'WRW'            

            return

        if (move == 'O-O-O' and player == 'W'):

            self.chess_board[self.initial_WK_rank][self.initial_WK_file] = 'B'
            self.chess_board[self.initial_WK_rank][self.initial_WK_file - 2] = 'WKB'

            self.chess_board[self.initial_WK_rank][self.initial_WK_file - 4] = 'B'
            self.chess_board[self.initial_WK_rank][self.initial_WK_file - 1] = 'WRW'            

            return            

        if (move == 'O-O' and player == 'B'):

            self.chess_board[self.initial_BK_rank][self.initial_BK_file] = 'W'
            self.chess_board[self.initial_BK_rank][self.initial_BK_file + 2] = 'BKW'

            self.chess_board[self.initial_BK_rank][self.initial_BK_file + 3] = 'B'
            self.chess_board[self.initial_BK_rank][self.initial_BK_file + 1] = 'BRB'            
            
            return            
        
        if (move == 'O-O-O' and player == 'B'):

            self.chess_board[self.initial_BK_rank][self.initial_BK_file] = 'W'
            self.chess_board[self.initial_BK_rank][self.initial_BK_file - 2] = 'BKW'

            self.chess_board[self.initial_BK_rank][self.initial_BK_file - 4] = 'W'
            self.chess_board[self.initial_BK_rank][self.initial_BK_file - 1] = 'BRB'            
            
            return

        
        simplified_move = self.get_move(move, player)

        piece = self.chess_board[simplified_move[0][0]][simplified_move[0][1]]
        final_square = self.chess_board[simplified_move[1][0]][simplified_move[1][1]]
        final_square = final_square[len(final_square) - 1]

        self.chess_board[simplified_move[0][0]][simplified_move[0][1]] = piece[len(piece) - 1]
        self.chess_board[simplified_move[1][0]][simplified_move[1][1]] = piece[0:len(piece)-1] + final_square

    def search_location_queen(self, rank, file):
        valid_positions = []

        for _rank in range(self.chess_squares):
            valid_positions.append((_rank, file))
        
        for _file in range(self.chess_squares):
            valid_positions.append((rank, _file))

        for i in range(self.chess_squares):
            if ( file + i < self.chess_squares and rank + i < self.chess_squares):
                valid_positions.append(( rank + i, file + i))

            if ( file + i < self.chess_squares and rank - i >= 0):
                valid_positions.append((rank - i, file + i))

            if ( file - i >= 0 and rank + i < self.chess_squares):
                valid_positions.append((rank + i, file - i))

            if ( file - i >= 0 and rank - i >= 0):
                valid_positions.append((rank - i, file - i))

        return valid_positions

    def search_location_rook(self, rank, file):
        valid_positions = []

        for _rank in range(self.chess_squares):
            valid_positions.append((_rank, file))
        
        for _file in range(self.chess_squares):
            valid_positions.append((rank, _file))

        return valid_positions        


    def search_location_bishop(self, rank, file):
        valid_positions = []

        for i in range(self.chess_squares):
            if ( file + i < self.chess_squares and rank + i < self.chess_squares):
                valid_positions.append((rank + i, file + i))

            if ( file + i < self.chess_squares and rank - i >= 0):
                valid_positions.append((rank - i, file + i))

            if ( file - i >= 0 and rank + i < self.chess_squares):
                valid_positions.append((rank + i, file - i))

            if ( file - i >= 0 and rank - i >= 0):
                valid_positions.append((rank - i, file - i))

        return valid_positions           

    def search_location_pawn_capture(self, rank, file, player):
        valid_positions = []

        if (player == 'W'):
            if ( file - 1 >= 0 and rank + 1 < self.chess_squares):
                valid_positions.append((rank + 1, file - 1))

            if ( file + 1 < self.chess_squares and rank + 1 < self.chess_squares):
                valid_positions.append((rank + 1, file + 1))

        else:
            if ( file - 1 >= 0 and rank - 1 >= 0):
                valid_positions.append((rank - 1, file - 1))

            if ( file + 1 < self.chess_squares and rank - 1 >= 0):
                valid_positions.append((rank - 1, file + 1))                

        return valid_positions            


    def search_location_pawn(self, rank, file, player):
        valid_positions = []

        if (player == 'W'):
            if (rank + 1 < self.chess_squares):
                valid_positions.append((rank + 1, file))

            if (rank + 2 < self.chess_squares):
                valid_positions.append((rank + 2, file))                
        else:
            if (rank - 1 >= 0):
                valid_positions.append((rank - 1, file))

            if (rank - 2 >= 0):
                valid_positions.append((rank - 2, file))                            

        return valid_positions

    def search_location_knight(self, rank, file):
        valid_positions = []

        if ( file + 1 < self.chess_squares and rank + 2 < self.chess_squares):
            valid_positions.append((rank + 2, file + 1))

        if ( file + 2 < self.chess_squares and rank + 1 < self.chess_squares):
            valid_positions.append((rank + 1, file + 2))

        if ( file - 1 >= 0 and rank + 2 < self.chess_squares):
            valid_positions.append((rank + 2, file - 1))

        if ( file - 2 >= 0 and rank + 1 < self.chess_squares):
            valid_positions.append((rank + 1, file - 2))            

        if ( file - 1 >= 0 and rank - 2 >= 0):
            valid_positions.append((rank - 2, file - 1))

        if ( file - 2 >= 0 and rank - 1 >= 0):
            valid_positions.append((rank - 1, file - 2))

        if ( file + 1 < self.chess_squares and rank - 2 >= 0):
            valid_positions.append((rank - 2, file + 1))

        if ( file + 2 < self.chess_squares and rank - 1 >= 0):
            valid_positions.append((rank - 1, file + 2))                               

        return valid_positions


    def search_location_king(self, rank, file):
        valid_positions = []

        if ( file + 1 < self.chess_squares and rank + 1 < self.chess_squares):
            valid_positions.append((rank + 1, file + 1))

        if ( rank + 1 < self.chess_squares):
            valid_positions.append((rank + 1, file))

        if ( file - 1 >= 0 and rank + 1 < self.chess_squares):
            valid_positions.append((rank + 1, file - 1))

        if ( file + 1 < self.chess_squares and rank - 1 >= 0):
            valid_positions.append((rank - 1, file + 1))

        if ( file - 1 >= 0 and rank - 1 >= 0):
            valid_positions.append((rank - 1, file - 1))                       

        if ( rank - 1 >= 0):
            valid_positions.append((rank - 1, file))

        if ( file - 1 >= 0):
            valid_positions.append((rank, file - 1))

        if ( file + 1 < self.chess_squares):
            valid_positions.append((rank, file + 1))                             

        return valid_positions                        