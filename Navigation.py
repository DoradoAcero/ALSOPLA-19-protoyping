"""
movies.py
created by lachlan on 27/8/19
"""

from tkinter import *
from tkinter.scrolledtext import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter import ttk

class Navigation:
    def __init__(self, __parent):
        self.__parent = __parent
        

class User:
    def __init__(self, ratings):
        self.__ratings = ratings

    def rate(self, movie, rating):
        self.__ratings[movie] = rating

    def get_ratings(self):
        return self.__ratings

class Movie:
    def __init__(self, identification, name, genres):
        self.__id = identification
        self.__name = name
        self.__genres = genres.split("|")

    def get_genres(self):
        return self.__genres

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__id


if __name__ == "__main__":
    root = Tk()
    Navigation(root)
    root.mainloop()
