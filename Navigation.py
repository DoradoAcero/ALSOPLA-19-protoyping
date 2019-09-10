"""
movies.py
created by lachlan on 27/8/19
"""

from tkinter import *
from tkinter.scrolledtext import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter import ttk
#from classic_set_engine import Engine
#from weighted_set_engine import Engine
from weighted_genre_set_engine import Engine
import time

class Navigation:
    
    def __init__(self, __parent):
        """The main rountine of the navigation classs"""
        self.__parent = __parent
        self.__users = []
        self.__movies = []
        self.__NUMBER_RECCOMENDATIONS = 5
        # This is creating a brand new user
        self.__MAIN_USER = User({},0)
        self.__users.append(self.__MAIN_USER)
        
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
        self.__users.append(User(ratings, user))
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
        # Setting up the engine, in this current version there is only the classic set engine, I need to think about how to change but given i only have the set engine i will not think about that yet
        self.__engine = Engine(self.__users, self.__movies, self.__MAIN_USER)
        print("Engine setup\n")
        print("Setup time taken,", time.time() - old, "\n")
        self.__possibilities = self.__engine.get_possibilities()

        # Setting up the GUI
        
        # Setting up the intial frames
        self.__reccomend_frame = Frame(self.__parent)
        self.__search_frame = Frame(self.__parent)
        self.__rate_frame = Frame(self.__parent)
        
        # Setting up the search
        self.__search_variable = StringVar()
        self.__search_entry = Entry(self.__parent, textvariable = self.__search_variable)
        self.__search_entry.grid(row=0, column=0, sticky="WENS")

        self.__search_button = Button(self.__parent, text="Search", command=self.search)
        self.__search_button.grid(row=0, column=1, sticky="WE")

        self.reccomend()

        # Making the Quit frame
        self.__exit_frame = Frame(self.__parent)
        self.__exit_button = Button(self.__exit_frame, text="Quit", command=self.quit)
        self.__back_button = Button(self.__exit_frame, text="Back", command=self.back)
        self.__exit_button.grid(column=0, row=0, sticky="WE")
        self.__back_button.grid(column=1, row=0, sticky="WE")
        self.__exit_frame.grid(column=0, row=2, columnspan=2)

    def reccomend(self):
        """The reccomendations"""
        # Setting up the intial reccomendations
        self.__reccomend_frame.grid(row=1, column=0, columnspan=2)
        self.__reccomend_label = Label(self.__reccomend_frame, text="Reccommended Movies\nMovie:    Percentage Rating:")
        self.__reccomend_label.grid(row=0, column=0, sticky="WE")
        self.__reccomend_labels = []
        
        # Making the reccomendation labels
        for possibility, movie in self.__possibilities[-self.__NUMBER_RECCOMENDATIONS:]:
            self.__reccomend_labels.append(Label(self.__reccomend_frame, text="{},    {}%".format(movie.get_name(), self.percentage(possibility))))
    
        for i in range(len(self.__reccomend_labels)):
            self.__reccomend_labels[i].grid(row=6-i, column=0, sticky="WE")

    def rate(self, movie):
        """the function to intiate the rating of a given movie"""
        self.clear()
        # Just setting up the GUI elements to input and confirm a rating for a given movie
        self.__head_label = Label(self.__rate_frame, text="Rate {}".format(movie.get_name()))
        self.__head_label.grid(column=0, row=0, columnspan=2, sticky="WE")

        self.__rate_variable = StringVar()
        self.__rate_entry = Entry(self.__rate_frame, textvariable = self.__rate_variable)
        self.__rate_entry.grid(row=1, column=0, sticky="WENS")
        self.__rate_label = Label(self.__rate_frame, text="A rating from 0-10\n(integers only)")
        self.__rate_label.grid(column=1, row=1, sticky="WE")
        self.__confirm_button = Button(self.__rate_frame, text="Rate", command=lambda :self.final_rate(movie))
        self.__confirm_button.grid(column=0, row=2, columnspan=2, sticky="WE")

        self.__rate_frame.grid(column=0, row=1, columnspan=2)

    def final_rate(self, movie):
        """the function to update the rating of the movie for the user"""
        
        # Updating the users ratings
        self.__MAIN_USER.rate(movie.id, int(int(self.__rate_variable.get())/2))
        
        # Updating the engine to accomodate
        self.__engine = Engine(self.__users, self.__movies, self.__MAIN_USER)
        self.__possibilities = self.__engine.get_possibilities()

        # Going back to the main menu
        self.back()

    def search(self):
        """The function to search based on the given text"""
        self.clear()
        self.__search_movies = []
        self.__search_labels = []
        self.__search_buttons = []
        # Putting the movies that match the search into a list
        for movie in self.__movies:
            if self.__search_variable.get().upper() in movie.get_name().upper():
                if not movie.id in self.__MAIN_USER.get_ratings().keys():
                    self.__search_movies.append(movie)
        if len(self.__search_movies) > 10:
            self.__search_movies = self.__search_movies[0:9]
            
        for i in range(len(self.__search_movies)):
            self.__search_labels.append(Label(self.__search_frame, text="{}    {}%".format(self.__search_movies[i].get_name(), self.percentage(self.__engine.possibility(self.__search_movies[i])))))
            
        # To all who read this, I'm sorry, looping it didnt work and this was the only option, I am probably dead from having to live with writing this horror, move on now so you dont suffer the same miserable end.
        if len(self.__search_movies) > 9:
            self.__search_buttons.append(Button(self.__search_frame, text="Rate {}".format(self.__search_movies[9].get_name()), command=lambda :self.rate(self.__search_movies[9])))
            
        if len(self.__search_movies) > 8:
            self.__search_buttons.append(Button(self.__search_frame, text="Rate {}".format(self.__search_movies[8].get_name()), command=lambda :self.rate(self.__search_movies[8])))
            
        if len(self.__search_movies) > 7:
            self.__search_buttons.append(Button(self.__search_frame, text="Rate {}".format(self.__search_movies[7].get_name()), command=lambda :self.rate(self.__search_movies[7])))
            
        if len(self.__search_movies) > 6:
            self.__search_buttons.append(Button(self.__search_frame, text="Rate {}".format(self.__search_movies[6].get_name()), command=lambda :self.rate(self.__search_movies[6])))
            
        if len(self.__search_movies) > 5:
            self.__search_buttons.append(Button(self.__search_frame, text="Rate {}".format(self.__search_movies[5].get_name()), command=lambda :self.rate(self.__search_movies[5])))
            
        if len(self.__search_movies) > 4:
            self.__search_buttons.append(Button(self.__search_frame, text="Rate {}".format(self.__search_movies[4].get_name()), command=lambda :self.rate(self.__search_movies[4])))
            
        if len(self.__search_movies) > 3:
            self.__search_buttons.append(Button(self.__search_frame, text="Rate {}".format(self.__search_movies[3].get_name()), command=lambda :self.rate(self.__search_movies[3])))
            
        if len(self.__search_movies) > 2:
            self.__search_buttons.append(Button(self.__search_frame, text="Rate {}".format(self.__search_movies[2].get_name()), command=lambda :self.rate(self.__search_movies[2])))
            
        if len(self.__search_movies) > 1:
            self.__search_buttons.append(Button(self.__search_frame, text="Rate {}".format(self.__search_movies[1].get_name()), command=lambda :self.rate(self.__search_movies[1])))
            
        if len(self.__search_movies) > 0:
            self.__search_buttons.append(Button(self.__search_frame, text="Rate {}".format(self.__search_movies[0].get_name()), command=lambda :self.rate(self.__search_movies[0])))
        
        if len(self.__search_movies) != 0:
            for i in range(len(self.__search_labels)):
                self.__search_labels[i].grid(row=i+1, column=0, sticky="WE")
                self.__search_buttons[i].grid(row=len(self.__search_labels)-i, column=1, sticky="WE")

        # Putting the heading label on
        message = "Movie:    Possibility Percentage:"
        if len(self.__search_labels) == 0:
            message = "There were no movies that matched your search!"
            
        self.__head_label = Label(self.__search_frame, text=message)
        self.__head_label.grid(row=0, column=0)
        self.__search_frame.grid(column=0, row=1, columnspan=2)
        
    def clear(self):
        """The function to remove the main frame"""
        try:
            self.__reccomend_frame.grid_forget()
        except:
            pass

        try:
            self.__search_frame.grid_forget()
            self.__head_label.grid_forget()
            for i in range(len(self.__search_labels)):
                self.__search_labels[i].grid_forget()
                self.__search_buttons[i].grid_forget()
            self.__search_labels = []
            self.__search_buttons = []
        except:
            pass

        try:
            self.__rate_frame.grid_forget()
        except:
            pass

    def percentage(self, index):
        """Given a index it returns the percentile it is in in the range of ratings"""
        range_indexs = self.__possibilities[-1][0] - self.__possibilities[0][0]
        percentage = round(100*(-self.__possibilities[0][0]+index)/range_indexs)
        return percentage

    def quit(self):
        self.__parent.destroy()

    def back(self):
        self.clear()
        self.reccomend()
        self.__reccomend_frame.grid(row=1, column=0)

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
        self.__rate(movie)

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
