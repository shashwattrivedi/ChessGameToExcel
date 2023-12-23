import argparse
import json
import os
from time import sleep

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

from ChessBoardCsvCreater import ChessBoardCsvCreater

import win32com.client as wincl

def main(moves_file_path, pieces_dir, game_dir):
    moves = []

    with open(moves_file_path, 'r') as moves_file:
        for move in moves_file:
            move = move.replace('+','')
            moves.append(move.split())

    chess_board_creater = ChessBoardCsvCreater(pieces_dir, game_dir)
    chess_board_creater.create_chess_board_csv(0, '')

    for move_num, move in enumerate(moves):
        chess_board_creater.execute_move(move[0], 'W')
        chess_board_creater.create_chess_board_csv(move_num + 1, 'W')

        if ( len(move) > 1 ):
            chess_board_creater.execute_move(move[1], 'B')
            chess_board_creater.create_chess_board_csv(move_num + 1, 'B')

    writer = pd.ExcelWriter(game_dir + '\game.xlsx', engine='xlsxwriter')
    game_move_files = []
    for game_move_filename in os.listdir(game_dir):
        if game_move_filename.endswith(".csv"):
            game_move_files.append(game_dir + "\\" + game_move_filename)
        else:
            continue

    df = pd.read_csv(game_dir + "\\" + "0.csv", header= None)
    df.to_excel(writer, sheet_name=str(0), header = False, index = False)

    for game_move in range(1, len(game_move_files)):

        for player in ['W','B'] :
            game_move_file = game_dir + "\\" + str(game_move) + str(player) + ".csv"
            
            if (game_move_file in game_move_files):
                df = pd.read_csv(game_move_file, header= None)
                df.to_excel(writer, sheet_name=str(game_move) + str(player), header = False, index = False)
            else:
                break

    workbook  = writer.book
    workbook.filename = game_dir + '\game.xlsm'
    workbook.add_vba_project('vbaProject.bin')

    writer.close()       

    runMacro(game_dir, "updateColourForAllSheets")
    runMacro(game_dir, "FormatCells")

def runMacro(game_dir, macro_name):

    if os.path.exists(game_dir + "\game.xlsm"):

        # DispatchEx is required in the newest versions of Python.
        excel_macro = wincl.DispatchEx("Excel.application")
        excel_path = os.path.expanduser(game_dir + "\game.xlsm")
        workbook = excel_macro.Workbooks.Open(Filename = excel_path, ReadOnly =1)
        excel_macro.Application.Run(macro_name)
        workbook.Save()
        excel_macro.Application.Quit()  
        del excel_macro

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Provide the moves file, pieces description dir and game dir')
    parser.add_argument('moves_file_path', help='moves_file_path')
    parser.add_argument('pieces_dir', help='directory containing description for pieces')
    parser.add_argument('game_dir', help='final game directory for saving csv')
    args = parser.parse_args()

    main(args.moves_file_path, args.pieces_dir, args.game_dir)
