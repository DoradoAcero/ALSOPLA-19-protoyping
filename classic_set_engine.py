"""
classic_set_engine.py
created by lachlan on 28/8/19
"""
import heapq


class Set_engine:
    
    def __init__(self, users, movies, user):
        """the main routine of the engine"""
        # Setting the current user

        self.__USER = users[user-1]

        # Setting the similarity indexes

        self.__similarity_index = {}
        print("Setting up similiarity index")
        for user in users:
            if user == self.__USER: # Not the user being selected for
                pass
            else:
                self.__similarity_index[user] = self.similarity(user)
        print("Similiarity index setup\n")
        print("Setting up possibility index")
        self.__possibility_index = {}
        for movie in movies:
            self.__possibility_index[movie] = self.possibility(movie)
        print("Possibility index setup\n")

    def similarity(self, user):
        """judges the similarity of a user to the main user"""
        agree = len(user.get_liked() & self.__USER.get_liked()) + len(user.get_disliked() & self.__USER.get_disliked())
        disagree = len(user.get_liked() & self.__USER.get_disliked()) + len(user.get_disliked() & self.__USER.get_liked())
        total = len(user.get_liked() | self.__USER.get_disliked() | user.get_disliked() | self.__USER.get_liked())
        return (agree-disagree)/total # Calculated by how much they agree vs disagree over the range that they can agree/disagree on

    def possibility(self, movie):
        """loops through the users in the possibility index and evaluates the movie given"""
        # Setting variables
        liked = 0
        disliked = 0
        likes = 0
        dislikes = 0
        for user in self.__similarity_index.keys():
            if movie.id in user.get_liked():
                liked += self.__similarity_index[user]
                likes += 1
            if movie.id in user.get_disliked():
                disliked += self.__similarity_index[user]
                dislikes += 1
        if likes+dislikes != 0:
            return (liked-disliked)/(likes+dislikes)
        else:
            return 0

    def get_possibility(self):
        length = len(self.__possibility_index)
        values = heapq.nlargest(length, self.__possibility_index.values())
        final_movies = []
        for i in range(length):
            for key in self.__possibility_index.keys():
                if self.__possibility_index[key] == values[i]:
                    if not key in final_movies:
                        final_movies.append(key)
        return [final_movies, values]

    def reccommend(self, reccomend):
        """Reccommend the main user movies"""
        values = heapq.nlargest(reccomend, self.__possibility_index.values())
        final_movies = []
        for i in range(reccomend):
            for key in self.__possibility_index.keys():
                if self.__possibility_index[key] == values[i]:
                    if not key in final_movies:
                        final_movies.append(key)
        return [final_movies, values]

