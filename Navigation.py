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
    """the main operating function/class of the prototype"""
    def __init__(self, __parent):
        self.__parent = __parent
        self.__users = []
        # Importing the lines of the csv file\
#         import csv
#         with open("ratings.csv") as csv_file:
#             csv_reader = csv.reader(csv_file, delimiter=",", encoding="utf-8")
#             line_0 = True
#             user = 1
#             ratings = {}
#             for row in csv_reader:
#                 if line_0:
#                     print(f"Column name are {", ".join(row)}")
#                     line_0 = False
#                 else:
#                     if user == row:
#                           self.__users.append(User(ratings, user))
                          
        
        

class User:
    """the assisting class that stores a user and all its properties"""
    UPPER_RATING = 4
    LOWER_RATING = 2
    
    """Despite the current iteration of engine only using
    likes and dislikes, i will keep the ratings in and process it in class"""
    
    def __init__(self, ratings, identification):
        """sets up the intial variables and the intial sets"""
        self.id = identification
        self.__ratings = ratings
        self.__liked = set()
        self.__disliked = set()
        for movie in self.__ratings.keys():
            self.__rate(movie)
    
    def __rate(self, movie):
        """Given a movie, put it into a like or disliked set"""
        if self.__ratings[movie] >= UPPER_RATING:
            self.likes(movie)
        elif self.__ratings[movie] <= LOWER_RATING:
            self.dislikes(movie)
                
    def likes(self, movie):
        """add a movie to the liked set"""
        self.__liked.add(movie)
    
    def dislikes(self, movie):
        """add a movie to the disliked set"""
        self.__disliked.add(movie)
        
    def rate(self, movie, rating):
        """add a movie to the rating dict, and then a corresponding (dis)liked set"""
        self.__ratings[movie] = rating
        self.rate(movie)

    def get_ratings(self):
        """helper method for accessing the dict"""
        return self.__ratings
    
    def get_liked(self):
        """helper method for accessing the liked set"""
        return self.__liked
    
    def get_disliked(self):
        """helper method for accessing the disliked set"""
        return self.__disliked

class Movie:
    """The assisting class that stores a movies properties"""
    def __init__(self, identification, name, genres):
        """setting up the variables for the movie"""
        self.id = identification
        self.__name = name
        self.__genres = genres.split("|")

    def get_genres(self):
        """helper method for accessing the genres"""
        return self.__genres

    def get_name(self):
        """helper method for accessing the name"""
        return self.__name


if __name__ == "__main__":
    root = Tk()
    Navigation(root)
    root.mainloop()
