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
        return len(self.participants)

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
    
    def getParticipantsFilterByPoints(self, participants, points):
        validateParticipants = []
        for participant in participants:
            if participant.points == points:
                validateParticipants.append(participant)
        return validateParticipants

    def getParticipantsSortByTieBreaker(self):
        return self.triParticipants("byTieBreaker")
    """FIN PARTICIPANT"""


    """DEROULEMENT TOURNOI"""
    #Début d'un tournoi (RESET)
    def startTournoi(self):
        # random.shuffle(self.participants)
        self.nbRound, self.top = self.calculNbRound(len(self.participants))
        self.started = False if self.nbRound == None  else True
        self.resetTournoi()
        return self.nbRound, self.top
    
    #Nouveau Round
    def newRound(self):
        havePlayed = False
        self.roundNumber = len(self.rondes) + 1

        # if self.roundNumber == 1:  # S'il s'agit du premier round
            # random.shuffle(self.participants)

        self.participants = self.adjustParticipant()
        participants = self.filteredParticipantsByNonDrop()

        ronde = Ronde(self.roundNumber)
        for i in range(0, len(participants), 2):
            if not havePlayed:
                firstParticipant = participants[i]
            else:
                firstParticipant = participants[i - 1]
            if i + 1 >= len(participants):
                secondParticipant = Participant(True)
                win = 0
            else:
                havePlayed = False
                secondParticipant = participants[i + 1]
                if len(participants) > i + 2:
                    if self.havePlayed(firstParticipant, participants[i + 1]):
                        if self.samePoints(firstParticipant, participants[i + 2]) or (not self.samePoints(firstParticipant, participants[i + 2]) and len(self.getParticipantsFilterByPoints(participants, participants[i + 2].points)) % 2 == 1):
                            havePlayed = True
                            secondParticipant = participants[i + 2]
                win = None
            finished = False
            if firstParticipant.drop == True or secondParticipant.drop == True:
                finished = True

            if finished == True:
                ronde.finishedTables += 1
            
            firstParticipant.newAdv(secondParticipant)
            secondParticipant.newAdv(firstParticipant)
            ronde.newTable(firstParticipant, secondParticipant, win, finished)

        self.rondes.append(ronde)
        self.startedRonde = True
        return ronde
    
    def adjustParticipant(self):
        listPoints = []
        for participant in self.participants:
            if participant.points not in listPoints:
                listPoints.append(participant.points)
        listPoints.sort(reverse=True) # reverse=False : asc // reverse=True : desc
        participants = []
        for point in listPoints:
            samePointParticipants = self.getParticipantsFilterByPoints(self.participants, point)
            lengthParticipant = len(samePointParticipants)
            lengthFirstGroupe = lengthParticipant // 2 + (lengthParticipant % 2)
            lengthSecondGroupe = lengthParticipant // 2
            firstGroupe = samePointParticipants[:lengthFirstGroupe]
            secondGroupe = samePointParticipants[lengthFirstGroupe:lengthFirstGroupe+lengthSecondGroupe]
            finalPointParticipants = []
            for i in range(max(len(firstGroupe), len(secondGroupe))):
                if i < len(firstGroupe):
                    finalPointParticipants.append(firstGroupe[i])
                if i < len(secondGroupe):
                    finalPointParticipants.append(secondGroupe[i])
            participants.extend(finalPointParticipants)
        return participants

    def havePlayed(self, participant1, participant2):
        return participant2 in participant1.adversaires or participant1 in participant2.adversaires
    
    def samePoints(self, participant1, participant2):
        return participant1.points == participant2.points
    
    #Retrie les joueurs selon leurs tieBreaker
    def triParticipants(self, filter):
        if filter == "byPoints":
            return sorted(self.participants, key=lambda x: x.points, reverse=True)
        if filter == "byTieBreaker":
            return sorted(self.participants, key=lambda x: x.tieBreaker, reverse=True)
    
    def triParticipantsByDrop(self):
        return sorted(self.participants, key=lambda x: x.drop)
    
    def filteredParticipantsByNonDrop(self):
        return [participant for participant in self.participants if not participant.drop]
    
    #Retourne une ronde
    def getRonde(self, rondeNumber):
        if rondeNumber > len(self.rondes) or rondeNumber < 0:
            return None
        else:
            if rondeNumber == 0:
                return self.rondes[len(self.rondes) - 1]
            else:
                return self.rondes[rondeNumber - 1]
    
    def goBackRonde(self):
        self.startedRonde = True

    #Définir le vainqueur
    def winner(self, tableNumber, pseudo):
        ronde = self.rondes[len(self.rondes) - 1]
        
        if tableNumber > len(ronde.tables):
            return "no-table"
        
        table = ronde.tables[tableNumber - 1]
        if not table.isInTable(pseudo) and not pseudo.upper() == "DRAW":
            return "no-player"
        
        if table.finished and not table.draw:
            for i in range(0, len(table.participants), 1):
                participant = table.participants[i]
                if (participant.pseudo.upper() == pseudo.upper() and table.win == i) or table.bye == True:
                    return "no-change"
            self.changeWinner(table)
            return "change"
        
        table.finished = True
        ronde.finishedTables += 1
        if pseudo.upper() == "DRAW":
            table.draw = True
            return "set-draw"
        else: 
            table.draw = False
        
        for i in range(0, len(table.participants), 1):
            participant = table.participants[i]
            if participant.pseudo.upper() == pseudo.upper():
                table.win = i
            else:
                table.win = 1 if i == 0 else 0
        return "set-winner"

    #Changer le vainqueur
    def changeWinner(self, table):
        table.win = 1 if table.win == 0 else 0

    #Si les tables ont fini de jouer
    def allFinishedTable(self):
        ronde = self.rondes[self.roundNumber - 1]
        return ronde.allFinishedTable()
    
    def dropPlayer(self, participant):
        participant.drop = True
    
    #Reset le tournoi
    def resetTournoi(self, stopTournoi = False):
        if stopTournoi:
            self.started = False
        self.name = ""
        self.startedRonde = False
        del self.rondes[:]
        self.roundNumber = 0
        for participant in self.participants:
            participant.win = 0
            participant.draw = 0
            participant.lose = 0
            participant.bye = 0
            participant.drop = False
            participant.points = 0
            participant.tieBreaker = 0
            participant.adversaires = []
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
            participant.defineStat()
            points = participant.win * regle.win + participant.draw * regle.draw + participant.lose * regle.lose + participant.bye * regle.bye
            firstStep = self.winRateCalcul(participant)
            secondStep = 0
            for adversaire in participant.adversaires:
                secondStep += self.winRateCalcul(adversaire)
            secondStep * 100 / len(participant.adversaires)
            participant.points = points
            participant.tieBreaker = points * 1_000_000 + firstStep * 1_000 + secondStep * 1
        endedTournoi = self.verifEndTournoi()
        if endedTournoi:
            return self.participants[0].pseudo
        else:
            return self.nbRound - self.roundNumber

    #Calcul de win Rate   
    def winRateCalcul(self, player):
        return player.win * 100 / self.roundNumber
    
    #Verification de fin de partie
    def verifEndTournoi(self):
        self.participants = self.triParticipants("byPoints")
        if self.nbRound == self.roundNumber or not self.participants[0].points == self.participants[1].points:
            return True
        return False
    
    """FIN CALCULS"""