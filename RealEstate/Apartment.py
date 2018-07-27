import pandas

class Apartment:
    def __init__(self, name):
        self.name = name
        log = pandas.DataFrame()
        log.columns = ['Year', 'Month', 'Label']

        self.cluster_log = log
