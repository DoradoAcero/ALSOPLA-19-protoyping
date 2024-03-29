

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
        """The main rountine of the navigation class"""
        self.__parent = __parent
        self.__users = []
        self.__movies = []
        self.__NUMBER_RECCOMENDATIONS = 5
        # This is creating a brand new user
        self.__MAIN_USER = User({},0)
        self.__users.append(self.__MAIN_USER)
        self.__parent.title("Movie Reccomendations")
        
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
                # Skip over line 1
                if line_0:
                    line_0 = False
                else:
                    # If the user is the correct user for the line
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
                    # Changing the "lakjsdhfi, The" formatting to "The lakjsdhfi" format
                    if ", The" in row[1]:
                        name = "The " + row[1]
                        commas = []
                        bracket = False
                        
                        for i in range(len(name)):
                            if not bracket:
                                if name[i] == ",":
                                    commas.append(i)
                                    
                                elif name[i] == "(":
                                    bracket = True
                        try:
                            final_name = name[:commas[-1]] + name[commas[-1]+5:] 
                            self.__movies.append(Movie(int(row[0]), final_name, row[2]))
                        except:
                            self.__movies.append(Movie(int(row[0]), row[1], row[2]))
                    else:
                        self.__movies.append(Movie(int(row[0]), row[1], row[2]))
                        
        print("{} movies imported\n".format(len(self.__movies)))
        print("Setting up engine")
        # Setting up the engine
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
        self.__search_entry.grid(row=0, column=0, sticky="WENS", ipadx=150)

        self.__search_button = Button(self.__parent, text="Search", command=self.search)
        self.__search_button.grid(row=0, column=1, sticky="WE")
        
        # Making the Quit buttons
        self.__exit_button = Button(self.__parent, text="Quit", command=self.quit)
        self.__back_button = Button(self.__parent, text="Back", command=self.back)
        self.__exit_button.grid(column=0, row=2, sticky="WE", ipadx=150)
        self.__back_button.grid(column=1, row=2, sticky="WE")
        self.genres()
        
        # Setting up the reccomendations
        self.math_setup()
        self.reccomend()

    def genres(self):
        # Making the genre buttons
        self.__genres = ['All', 'War', 'Mystery', 'Horror', 'IMAX', '(no genres listed)', 'Western', 'Thriller', 'Fantasy', 'Documentary', 'Adventure', 'Animation', 'Romance', 'Crime', 'Children', 'Action', 'Drama', 'Sci-Fi', 'Musical', 'Comedy', 'Film-Noir']
        self.__genre = StringVar()
        self.__genre_menu = ttk.Combobox(self.__reccomend_frame, textvariable=self.__genre, state="readonly")
        self.__genre_menu["values"] = sorted(self.__genres)
        self.__genre_menu.grid(column=3, row=1, sticky = "WE")
        self.__genre.trace("w", self.genre_reccomend)


    def math_setup(self):
        """Setting up the normal distribution variables to give user accesible ratings"""
        self.__mean = 0
        for possibility, movie in self.__possibilities:
            self.__mean += possibility
        self.__mean /= len(self.__possibilities)

        self.__std = self.__possibilities[round(len(self.__possibilities)*0.68)][0] - self.__mean
        

    def genre_reccomend(self, *args):
        genre = self.__genre.get()
        if genre == "All":
            self.reccomend()
        else:
            self.clear()
            genre_movies = []
            self.genres()
            self.__search_entry.grid(row=0, column=0, sticky="WENS", ipadx=150)
            self.__exit_button.grid(column=0, row=2, sticky="WE", ipadx=150)
            for possibility, movie in self.__possibilities:
                if genre in movie.get_genres():
                    genre_movies.append((possibility, movie))
            self.__reccomend_frame.grid(row=1, column=0, columnspan=2)
            
            self.__reccomend_label = Label(self.__reccomend_frame, text="Recommended Movies")
            self.__reccomend_label.grid(row=0, column=0, columnspan=3, sticky="WE")

            self.__genre_search_label = Label(self.__reccomend_frame, text="Genre Search:")
            self.__genre_search_label.grid(row=0, column=3, sticky="WE")

            label_texts = ["Movie:", "Genre:", "Percentage Match:"]

            self.__reccomend_headers = []
            for i in range(len(label_texts)):
                self.__reccomend_headers.append(Label(self.__reccomend_frame, text=label_texts[i]))
                self.__reccomend_headers[i].grid(row=1, column=i, sticky="WE")

            # 4 columns, so four lists and sublist to occupy
            self.__reccomend_labels = [[], [], []]
            self.__reccomend_buttons = []
            
            # Making the reccomendation labels
            for possibility, movie in genre_movies[-5:]:
                genres = ""
                for genre in movie.get_genres():
                    genres += "{}, ".format(genre)
                if len(movie.get_name()) > 60:
                    self.__reccomend_labels[0].append(Label(self.__reccomend_frame, text=movie.get_name()[:51]+"..."+movie.get_name()[-6:]))
                else:
                    self.__reccomend_labels[0].append(Label(self.__reccomend_frame, text=movie.get_name()))
                self.__reccomend_labels[1].append(Label(self.__reccomend_frame, text=genres[:-2]))
                self.__reccomend_labels[2].append(Label(self.__reccomend_frame, text="{}%".format(self.percentage(possibility))))
                
            for i in range(len(self.__reccomend_labels[0])):
                self.__reccomend_buttons.append(Button(self.__reccomend_frame, text="Rate", command=lambda x=i:self.rate(genre_movies[-(x+1)][1])))
        
            # gridding the labels and buttons
            for i in range(len(self.__reccomend_labels[0])):
                self.__reccomend_labels[0][i].grid(row=6-i, column=0, sticky="WE")
                self.__reccomend_labels[1][i].grid(row=6-i, column=1, sticky="WE")
                self.__reccomend_labels[2][i].grid(row=6-i, column=2, sticky="WE")
                self.__reccomend_buttons[i].grid(row=i+2, column=3, sticky="WE")

    def reccomend(self):
        """The reccomendations"""
        # Setting up the intial reccomendations
        self.clear()
        self.genres()
        self.__search_entry.grid(row=0, column=0, sticky="WENS", ipadx=150)
        self.__exit_button.grid(column=0, row=2, sticky="WE", ipadx=150)
        self.__reccomend_frame.grid(row=1, column=0, columnspan=2)
        
        self.__reccomend_label = Label(self.__reccomend_frame, text="Recommended Movies")
        self.__reccomend_label.grid(row=0, column=0, columnspan=3, sticky="WE")

        self.__genre_search_label = Label(self.__reccomend_frame, text="Genre Search:")
        self.__genre_search_label.grid(row=0, column=3, sticky="WE")

        label_texts = ["Movie:", "Genre:", "Percentage Match:"]

        self.__reccomend_headers = []
        for i in range(len(label_texts)):
            self.__reccomend_headers.append(Label(self.__reccomend_frame, text=label_texts[i]))
            self.__reccomend_headers[i].grid(row=1, column=i, sticky="WE")

        # 4 columns, so four lists and sublist to occupy
        self.__reccomend_labels = [[], [], []]
        self.__reccomend_buttons = []
        
        # Making the reccomendation labels
        for possibility, movie in self.__possibilities[-5:]:
            genres = ""
            for genre in movie.get_genres():
                genres += "{}, ".format(genre)
            if len(movie.get_name()) > 60:
                self.__reccomend_labels[0].append(Label(self.__reccomend_frame, text=movie.get_name()[:51]+"..."+movie.get_name()[-6:]))
            else:
                self.__reccomend_labels[0].append(Label(self.__reccomend_frame, text=movie.get_name()))
            self.__reccomend_labels[1].append(Label(self.__reccomend_frame, text=genres[:-2]))
            self.__reccomend_labels[2].append(Label(self.__reccomend_frame, text="{}%".format(self.percentage(possibility))))

        for i in range(len(self.__reccomend_labels[0])):
            self.__reccomend_buttons.append(Button(self.__reccomend_frame, text=" Rate ", command=lambda x=i:self.rate(self.__possibilities[-(x+1)][1])))
    
        # Gridding the labels and buttons
        for i in range(len(self.__reccomend_labels[0])):
            self.__reccomend_labels[0][i].grid(row=6-i, column=0, sticky="WE")
            self.__reccomend_labels[1][i].grid(row=6-i, column=1, sticky="WE")
            self.__reccomend_labels[2][i].grid(row=6-i, column=2, sticky="WE")
            self.__reccomend_buttons[i].grid(row=i+2, column=3, sticky="WE")

    def rate(self, movie):
        """the function to intiate the rating of a given movie"""
        self.clear()
        self.__search_entry.grid(row=0, column=0, sticky="WENS", ipadx=0)
        self.__exit_button.grid(column=0, row=2, sticky="WE", ipadx=0)
        # Just setting up the GUI elements to input and confirm a rating for a given movie
        self.__head_label = Label(self.__rate_frame, text="Rate {}".format(movie.get_name()))
        self.__head_label.grid(column=0, row=0, columnspan=2, sticky="WE")

        self.__rate_variable = StringVar()
        self.__rate_scale = Scale(self.__rate_frame, from_=0, to=5, resolution=0.1, orient=HORIZONTAL)
        self.__rate_scale.grid(row=1, column=0, sticky="WE")
        self.__confirm_button = Button(self.__rate_frame, text="Rate", command=lambda :self.final_rate(movie))
        self.__confirm_button.grid(column=0, row=2, columnspan=2, sticky="WE")

        self.__rate_frame.grid(column=0, row=1, columnspan=2, sticky="WE")

    def final_rate(self, movie):
        """the function to update the rating of the movie for the user"""
        
        # Updating the users ratings
        self.__MAIN_USER.rate(movie.id, float(self.__rate_scale.get()))
        
        # Updating the engine to accomodate
        self.__engine = Engine(self.__users, self.__movies, self.__MAIN_USER)
        self.__possibilities = self.__engine.get_possibilities()

        # Going back to the main menu
        
        self.math_setup()
        self.back()

    def search(self):
        """The function to search based on the given text"""
        self.clear()
        self.__search_entry.grid(row=0, column=0, sticky="WENS", ipadx=0)
        self.__exit_button.grid(column=0, row=2, sticky="WE", ipadx=0)
        self.__search_movies = []
        self.__search_labels = []
        self.__search_buttons = []
        # Putting the movies that match the search into a list
        for movie in self.__movies:
            if self.__search_variable.get().upper() in movie.get_name().upper():
                if not movie.id in self.__MAIN_USER.get_ratings().keys():
                    self.__search_movies.append(movie)
        if len(self.__search_movies) > 6:
            self.__search_movies = self.__search_movies[0:5]
            
        for i in range(len(self.__search_movies)):
            self.__search_labels.append(Label(self.__search_frame, text="{}    {}%".format(self.__search_movies[i].get_name(), self.percentage(self.__engine.possibility(self.__search_movies[i])))))
            
        # To all who read this, I'm sorry, looping it didnt work and this was the only option, I am probably dead from having to live with writing this horror, move on now so you dont suffer the same miserable end.
        for i in range(len(self.__search_movies)):
            self.__search_buttons.append(Button(self.__search_frame, text="Rate", command=lambda x=i:self.rate(self.__search_movies[i])))
        
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
        self.__search_variable.set("")
        
    def clear(self):
        """The function to remove the main frame"""
        try:
            self.__reccomend_frame.destroy()
            self.__reccomend_frame = Frame(self.__parent)
        except:
            pass

        try:
            self.__search_frame.destroy()
            self.__search_frame = Frame(self.__parent)
            self.__head_label.grid_forget()
            for i in range(len(self.__search_labels)):
                self.__search_labels[i].grid_forget()
                self.__search_buttons[i].grid_forget()
            self.__search_labels = []
            self.__search_buttons = []
        except:
            pass

        try:
            self.__rate_frame.destroy()
            self.__rate_frame = Frame(self.__parent)
        except:
            pass

    def percentage(self, index):
        """Given a index it returns the percentile it is in in the range of ratings"""
        number = len(self.__MAIN_USER.get_ratings())
        
        if number > 0:
            # The expected value of the natural falling of the percentages of the maximum possible index
            expected = (51+50/(2.718**(number**0.4)/5))

            # The percentage of the maximum possible index - expected to give a difference to multiply the accuracy expectation by
            change = 1 + (((100*(index/(1/number + 1))+100)/2)-expected)/100
            print(change)
            final = (99-100/(2.718**number))*change
            return round(final)
        else:
            # I said 0.1 cause thats about how confident i am in these preduictions
            return round((index*50+50)/10)

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
