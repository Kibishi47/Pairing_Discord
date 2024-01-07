# win == 0 => participant[0] a win
# win == 1 => participant[1] a win

class Table:
    def __init__(self, number, firstParticipant, secondParticipant, win, finished = False):
        self.number = number
        self.finished = finished
        self.win = win
        self.draw = False
        self.bye = finished
        self.participants = []
        self.participants.append(firstParticipant)
        self.participants.append(secondParticipant)

    def isInTable(self, pseudo):
        for participant in self.participants:
            if pseudo.upper() == participant.pseudo.upper():
                return True
        return False
    
    def get(self):
        return f"{self.participants[0].pseudo} VS {self.participants[1].pseudo}"