"""
movies.py
created by lachlan on 27/8/19
"""

from tkinter import *
from tkinter.scrolledtext import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter import ttk
from classic_set_engine import Set_engine

class Navigation:
    
    def __init__(self, __parent):
        """The main rountine of the navigation classs"""
        self.__parent = __parent
        self.__users = []
        self.__movies = []
        number_reccomendations = 5
        
        # Importing the lines of the csv file to init the users and the movies
        import csv
        import time
        old = time.time()
        print("Importing Users")
        with open("ratings.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_0 = True
            user = 1
            ratings = {}
            for row in csv_reader:
                if line_0:
                    line_0 = False
                else:
                    if user != int(row[0]):
                        self.__users.append(User(ratings, user))
                        ratings = {int(row[1]):float(row[2])}
                        user += 1
                    else:
                        ratings[int(row[1])] = float(row[2])
        print("{} users imported\n".format(len(self.__users)))
        print("Importing movies")
        with open("movies.csv", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_0 = True
            for row in csv_reader:
                if line_0:
                    line_0 = False
                else:
                    self.__movies.append(Movie(int(row[0]), row[1], row[2]))
        print("{} movies imported\n".format(len(self.__movies)))
        print("Setting up engine")
        self.__engine = Set_engine(self.__users, self.__movies, 6)
        print("Engine setup\n")
        print(time.time() - old, "\n")

        reccomendations = self.__engine.reccommend(number_reccomendations)
        #reccomendations = self.__engine.get_possibility()
        for i in range(len(reccomendations[0])):
            print(reccomendations[0][i].get_name(), reccomendations[1][i])
        
        

class User:
    """the assisting class that stores a user and all its properties"""
    
    
    """Despite the current iteration of engine only using
    likes and dislikes, i will keep the ratings in and process it in class"""
    
    def __init__(self, ratings, identification):
        """sets up the intial variables and the intial sets"""
        self.UPPER_RATING = 4
        self.LOWER_RATING = 2
        self.id = identification
        self.__ratings = ratings
        self.__liked = set()
        self.__disliked = set()
        for movie in self.__ratings.keys():
            self.__rate(movie)
    
    def __rate(self, movie):
        """Given a movie, put it into a like or disliked set"""
        if self.__ratings[movie] >= self.UPPER_RATING:
            self.likes(movie)
        elif self.__ratings[movie] <= self.LOWER_RATING:
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
