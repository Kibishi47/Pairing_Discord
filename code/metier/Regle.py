class Regle:
    def __init__(self):
        self.win = 3
        self.draw = 1
        self.lose = 0
        self.bye = 3
        self.rulesRound = [
            {"minJoueur": 4, "maxJoueur": 8, "nbRound": 3, "top": 0},
            {"minJoueur": 9, "maxJoueur": 16, "nbRound": 4, "top": 2},
            {"minJoueur": 17, "maxJoueur": 32, "nbRound": 5, "top": 4},
            {"minJoueur": 33, "maxJoueur": 64, "nbRound": 6, "top": 8},
            {"minJoueur": 65, "maxJoueur": 128, "nbRound": 7, "top": 8},
            {"minJoueur": 129, "maxJoueur": 256, "nbRound": 8, "top": 16},
            {"minJoueur": 257, "maxJoueur": 512, "nbRound": 9, "top": 16},
            {"minJoueur": 513, "maxJoueur": 1024, "nbRound": 10, "top": 32},
        ]
