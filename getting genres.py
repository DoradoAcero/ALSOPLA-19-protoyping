from Navigation import Movie
import csv

movies = []
genres = {}
with open("movies.csv", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_0 = True
            for row in csv_reader:
                if line_0:
                    line_0 = False
                else:
                    movies.append(Movie(int(row[0]), row[1], row[2]))

for movie in movies:
    for genre in movie.get_genres():
        genres[genre] = 0

print(genres)
