class Participant:
    def __init__(self, pseudo=""):
        self.nom = ""
        self.prenom = ""
        self.pseudo = pseudo
        self.win = 0
        self.draw = 0
        self.lose = 0
        self.bye = 0
        self.points = 0
        self.tieBreaker = 0
        self.adversaires = []

    def __str__(self):
        return f"Participant(nom = {self.nom}, prenom = {self.prenom}, pseudo = {self.pseudo})"
    
    def newAdv(self, adversaire):
        if adversaire.pseudo == "BYE":
            self.bye += 1
        self.adversaires.append(adversaire)

    def get(self):
        return {"nom" : self.nom, "prenom": self.prenom, "pseudo": self.pseudo}