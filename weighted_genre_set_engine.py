"""
weighted_genre_set_engine.py
created by lachlan on 10/9/19
"""


class Engine:
    
    def __init__(self, users, movies, user):
        """the main routine of the engine"""
        # Setting the current user

        self.__USER = user
        self.__similarity_index = {}
        self.__possibility_index = []
        self.__genre_index = {'Film-Noir': 0, 'Thriller': 0, 'Action': 0, 'Horror': 0, 'Mystery': 0, 'War': 0, 'Sci-Fi': 0, 'Drama': 0, 'Musical': 0, 'Fantasy': 0, 'Animation': 0, 'IMAX': 0, 'Documentary': 0, 'Romance': 0, 'Comedy': 0, '(no genres listed)': 0, 'Western': 0, 'Children': 0, 'Adventure': 0, 'Crime': 0}

        # Setting the indexes
        if len(self.__USER.get_ratings()) == 0:
            # General ratings for all movies
            for movie in movies:
                # For each movie record how many people liked and dislike the movie
                liked = 0
                disliked = 0
                for user in users:
                    if movie.id in user.get_liked():
                        liked += 1
                    elif movie.id in user.get_disliked():
                        disliked += 1
                # Dividing by zero will give an error, so just append 0
                if liked+disliked == 0:
                    self.__possibility_index.append((0, movie))
                else:
                    # Possibility index with similarities being 1
                    self.__possibility_index.append(((liked-disliked)/(liked+disliked), movie))
                
        else:
            # Specific rating for a user
            print("Setting up similiarity index")
            for user in users:
                if user == self.__USER: # Not the user being selected for
                    pass
                else:
                    # Put the user similarities into the index
                    self.__similarity_index[user] = self.similarity(user)
            print("Similiarity index setup\n")

            # Genre index updating
            for movie_id in self.__USER.get_ratings().keys():
                for movie in movies:
                    if movie.id == movie_id:
                        for genre in movie.get_genres():
                            # For the genre, iterate by the fraction of how above average it is based on the rating of the genre
                            self.__genre_index[genre] += (self.__USER.get_ratings()[movie_id]/2.5)-0.5
                
            print("Setting up possibility index")
            
            for movie in movies:
                if not movie.id in self.__USER.get_ratings().keys():
                    # Setup the possibility index
                    possibility = self.possibility(movie)
                    self.__possibility_index.append((possibility, movie))
                
        import operator
        self.__possibility_index.sort(key = operator.itemgetter(0))
        print("Possibility index setup\n")

    def similarity(self, user):
        """judges the similarity of a user to the main user"""
        similarity = 0
        for movie in user.get_ratings():
            if movie in self.__USER.get_ratings():
                # Difference in ratings
                difference = user.get_ratings()[movie] - self.__USER.get_ratings()[movie]

                # 2.5 - the absolute difference to give a general difference in rating of movie
                if difference < 0:
                    similarity += 2*(2.5+difference)
                else:
                    similarity += 2*(2.5-difference)
        # Original set math
        similarity /= len(user.get_liked() | self.__USER.get_disliked() | user.get_disliked() | self.__USER.get_liked())
        return similarity
                

    def possibility(self, movie):
        """loops through the users in the possibility index and evaluates the movie given"""
        # Setting variables
        possibility = 0
        ratings = 0
        for user in self.__similarity_index.keys():
            if movie.id in user.get_ratings():
                # Weight the possibility with the rating and the similarity index
                possibility += (self.__similarity_index[user]**2)*(user.get_ratings()[movie.id]-2.5)
                ratings += 1
                
        genre_possibility = 0
        for genre in movie.get_genres():
            # Find the amount of likeness to the users liked genres
            genre_possibility += self.__genre_index[genre]

        # Making sure there is no /0
        if ratings != 0:
            # possibility is normal, as number of movies rated, the weighting of genre decreases
            return possibility/ratings + genre_possibility/(len(self.__USER.get_ratings())**2)
        else:
            return 0

    def get_possibilities(self):
        """Get all the possibilities for all the movies"""
        return self.__possibility_index
        
    def reccommend(self, reccomend):
        """Reccommend the main user movies"""
        return self.__possibility_index[0:reccomend-1]
    
