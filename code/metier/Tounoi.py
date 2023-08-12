import random
from metier.Participant import Participant
from metier.Ronde import Ronde
from metier.Regle import Regle

class Tournoi:
    def __init__(self):
        self.name = ""
        self.started = False
        self.startedRonde = False
        self.participants = []
        self.rondes = []
        self.roundNumber = 0
        self.nbRound = 0
        self.top = 0

    """PARTICIPANT"""
    #Ajout d'un participant au tournoi
    def addParticipant(self, participant):
        self.participants.append(participant)

    #Effacement d'un ou tous les participants
    def clearParticipants(self, pseudo):
        if pseudo is None:
            del self.participants[:]
        else:
            self.participants = [participant for participant in self.participants if participant.pseudo.upper() != pseudo.upper()]

    #Recherche d'un participant
    def searchParticipant(self, pseudo):
        theParticipant = None
        for participant in self.participants:
            if participant.pseudo.upper() == pseudo.upper():
                theParticipant = participant
        return theParticipant
    
    """FIN PARTICIPANT"""


    """DEROULEMENT TOURNOI"""
    #Début d'un tournoi (RESET)
    def startTournoi(self):
        random.shuffle(self.participants)
        self.nbRound, self.top = self.calculNbRound(len(self.participants))
        self.started = False if self.nbRound == None else True
        del self.rondes[:]
        return self.nbRound, self.top
    
    #Nouveau Round
    def newRound(self):
        self.roundNumber = len(self.rondes) + 1
        if self.roundNumber == 1: #S'il s'agit du premier round
            random.shuffle(self.participants)
        else:
            self.triParticipants()
        ronde = Ronde(self.roundNumber)
        for i in range(0, len(self.participants), 2):
            firstParticipant = self.participants[i]
            if i + 1 >= len(self.participants):
                secondParticipant = Participant("BYE")
                win = 0
                finished = True
            else: 
                secondParticipant = self.participants[i + 1]
                win = None
                finished = False
            firstParticipant.newAdv(secondParticipant)
            secondParticipant.newAdv(firstParticipant)
            ronde.newTable(firstParticipant, secondParticipant, win, finished)
        self.rondes.append(ronde)
        self.startedRonde = True
        return ronde
    
    #Retrie les joueurs selon leurs tieBreaker
    def triParticipants(self):
        self.participants = sorted(self.participants, key=lambda x: x.tieBreaker, reverse=True)
    
    #Retourne une ronde
    def getRonde(self, rondeNumber):
        if rondeNumber > len(self.rondes) or rondeNumber < 0:
            return None
        else:
            if rondeNumber == 0:
                return self.rondes[len(self.rondes) - 1]
            else:
                return self.rondes[rondeNumber - 1]
    
    #Définir le vainqueur
    def winner(self, tableNumber, pseudo):
        ronde = self.rondes[len(self.rondes) - 1]
        
        if tableNumber > len(ronde.tables):
            return "no-table"
        
        table = ronde.tables[tableNumber - 1]
        if not table.isInTable(pseudo) and not pseudo.upper() == "DRAW":
            return "no-player"
        
        if table.finished and not table.draw:
            self.changeWinner(table, pseudo)
            return "change"
        
        table.finished = True
        ronde.finishedTables += 1
        if pseudo.upper() == "DRAW":
            table.draw = True
            for participant in table.participants:
                participant.draw += 1
            return "set-draw"
        else: 
            table.draw = False
        
        for i in range(0, len(table.participants), 1):
            participant = table.participants[i]
            if participant.pseudo.upper() == pseudo.upper():
                table.win = i
                participant.win += 1
            else:
                table.win = 1 if i == 0 else 0
                participant.lose += 1
        
        return "set-winner"

    #Changer le vainqueur
    def changeWinner(self, table, pseudo):
        table.win = 1 if table.win == 0 else 0
        for participant in table.participants:
            if participant.pseudo.upper() == pseudo.upper():
                participant.win += 1
                participant.lose -= 1
            else:
                participant.lose += 1
                participant.win -= 1

    #Si les tables ont fini de jouer
    def allFinishedTable(self):
        ronde = self.rondes[self.roundNumber - 1]
        return ronde.allFinishedTable()
    """FIN DEROULEMENT TOURNOI"""


    """CALCULS"""
    #Calcul nbRound
    def calculNbRound(self, nbJoueur):
        regle = Regle()
        for rule in regle.rulesRound:
            minJoueur = rule["minJoueur"]
            maxJoueur = rule["maxJoueur"]
            if minJoueur <= nbJoueur <= maxJoueur:
                return rule["nbRound"], rule["top"]
        return None, None

    #FIN DE ROUND
    #Calcul des points de chaque joueurs
    def calculPoints(self):
        self.startedRonde = False
        regle = Regle()
        for participant in self.participants:
            points = participant.win * regle.win + participant.draw * regle.draw + participant.lose * regle.lose + participant.bye * regle.bye
            firstStep = self.winRateCalcul(participant)
            secondStep = 0
            for adversaire in participant.adversaires:
                secondStep += self.winRateCalcul(adversaire)
            secondStep * 100 / len(participant.adversaires)
            participant.points = points
            participant.tieBreaker = points * 1_000_000 + firstStep * 1_000 + secondStep * 1
        self.triParticipants()
        endedTournoi = self.verifEndTournoi()
        if endedTournoi:
            self.started = False
            self.roundNumber = 0
            return self.participants[0].pseudo
        return self.nbRound - self.roundNumber

    #Calcul de win Rate   
    def winRateCalcul(self, player):
        return player.win * 100 / self.roundNumber
    
    #Verification de fin de partie
    def verifEndTournoi(self):
        if self.nbRound == self.roundNumber or not self.participants[0].points == self.participants[1].points:
            return True
        return False
    
    """FIN CALCULS"""