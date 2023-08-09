from metier.Table import Table

class Ronde:
    def __init__(self, number):
        self.number = number
        self.finishedTables = 0
        self.tables = []
    
    def newTable(self, firstParticipant, secondParticipant, win, finished):
        self.tables.append(Table(len(self.tables) + 1, firstParticipant, secondParticipant, win, finished))

    def allFinishedTable(self):
        if self.finishedTables == len(self.tables):
            return True
        return False