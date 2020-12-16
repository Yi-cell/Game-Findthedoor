
# Key Cave Adventure Game

""" Initialization """
GAME_LEVELS = {
    # dungeon layout: max moves allowed
    "game1.txt": 7,
    "game2.txt": 12,
    "game3.txt": 19,
}
PLAYER = "O"
KEY = "K"
DOOR = "D"
WALL = "#"
MOVE_INCREASE = "M"
SPACE = " "
DIRECTIONS = {
    "w": (-1, 0),
    "s": (1, 0),
    "d": (0, 1),
    "a": (0, -1)
}
INVESTIGATE = "I"
QUIT = "Q"
VALID_ACTIONS = [INVESTIGATE, QUIT, *DIRECTIONS.keys()]
INVALID = "That's invalid."
WIN_TEXT = "You have won the game with your strength and honour!"
LOSE_TEST = "You have lost all your strength and honour."



""" Import the packages """
import tkinter as tk
import time
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog

''' Put the main here'''


def main():
    root = tk.Tk()   
    GameApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()
