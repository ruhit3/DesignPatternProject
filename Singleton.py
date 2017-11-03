__author__ = "Azharuddin Ruhit"

class Movie:
    def __init__(self, id, name, genre):
        self.id = id
        self.name = name
        self.genre = genre

    def define(self):
        print(self.id, self.name, self.genre)


class Singleton:
    __instance = None

    movie_list = []
    preferences = {}

    def __init__(self):
        if Singleton.__instance != None:
            raise Exception("Singleton Class!")
        else:
            Singleton.__instance = self

    @staticmethod
    def getInstance(data, item, genre):
        #extracting genres
        genre_list = []
        for cat in genre:
            genre_list.append(cat[0:1][0])
        #mapping genres
        for mov in item:
            count = 0
            new_genre_list = []
            for i in mov[5:24]:
                if i != '0':
                    new_genre_list.append(genre_list[count])
                count += 1
            #creating a movie object
            movie = Movie(mov[0], mov[1][:-7], new_genre_list)
            Singleton.movie_list.append(movie)
        #reading preferences
        for pref in data:
            user, movieID, rating = pref[0:3]
            Singleton.preferences.setdefault(user, {})
            movie_name = ''
            for mov in Singleton.movie_list:
                if mov.id == movieID:
                    movie_name = mov.name
                    break
            Singleton.preferences[user][movie_name] = float(rating)
        #returning singleton instance
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance