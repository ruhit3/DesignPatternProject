import types


class StrategyParser:
    def __init__(self, func=None):
        self.filename = 'default'
        if func is not None:
            self.execute = types.MethodType(func, self)

    def execute(self):
        print(self.filename)


def tabParser(self):
    list = []
    for line in open(self.filename):
        list.append(line.split('\t'))
    return list


def pipeParser(self):
    list = []
    for line in open(self.filename):
        list.append(line.split('|'))
    return list


class LoadDataset:
    def __init__(self):
        pass

    def parseAll(self):
        strategy = StrategyParser(tabParser)
        strategy.filename = 'dataset/u.data'
        self.data = strategy.execute()
        strategy = StrategyParser(pipeParser)
        strategy.filename = 'dataset/u.item'
        self.item = strategy.execute()
        strategy = StrategyParser(pipeParser)
        strategy.filename = 'dataset/u.genre'
        self.genre = strategy.execute()


'''if __name__ == '__main__':
    dataset = LoadDataset()
    print(dataset.data[1])
    print(dataset.item[1])
    print(dataset.genre[1])'''