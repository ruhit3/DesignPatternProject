import Strategy
import Singleton


class Moviekit:
    def __init__(self):
        self.dataset = Strategy.LoadDataset()
        self.database = Singleton.Singleton()

    def start_app(self):
        self.dataset.parseAll()
        self.database.getInstance(self.dataset.data, self.dataset.item, self.dataset.genre)


'''if __name__ == '__main__':
    facade = Moviekit()
    facade.start_app()
    facade.database.movie_list[4].define()'''