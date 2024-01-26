class Participant:
    def __init__(self, drop=False):
        self.pseudo = ""
        self.drop = drop
        self.points = 0
        self.tieBreaker = 0
        self.adversaires = []
        self.tables = []
        self.resetStat()

    def __str__(self):
        return f"Participant(pseudo = {self.pseudo})"
    
    def newAdv(self, adversaire):
        if adversaire.drop:
            self.bye += 1
        self.adversaires.append(adversaire)

    def newTable(self, table):
        self.tables.append(table)
    
    def notInAdversaries(self, participant):
        return participant not in self.adversaires
    
    def resetStat(self):
        self.win = 0
        self.draw = 0
        self.lose = 0
        self.bye = 0
    
    def defineStat(self):
        self.resetStat()
        for table in self.tables:
            for i in range(0, len(table.participants), 1):
                participant = table.participants[i]
                if participant.pseudo.upper() == self.pseudo.upper():
                    if table.bye:
                        self.bye += 1
                    elif table.draw:
                        self.draw += 1
                    elif table.win == i:
                        self.win += 1
                    else:
                        self.lose += 1
                