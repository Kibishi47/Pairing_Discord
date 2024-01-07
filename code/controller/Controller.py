from metier.Tounoi import Tournoi
from model.DiscordBot import DiscordBot

class Controller:
    def __init__(self):
        self.tournoi = Tournoi()
        self.botDiscord = DiscordBot(self)

    """CONTROLE PARTICIPANT"""
    def newParticipant(self, participant):
        return self.tournoi.addParticipant(participant)

    def resetParticipant(self):
        self.tournoi.clearParticipant()

    def searchParticipant(self, pseudo):
        return self.tournoi.searchParticipant(pseudo)
    
    def getParticipants(self):
        return self.tournoi.participants
    
    def getSortedParticipants(self):
        return self.tournoi.getParticipantsSortByTieBreaker()
    
    def clearParticipants(self, pseudo):
        self.tournoi.clearParticipants(pseudo)
    
    """FIN CONTROLE PARTICIPANT"""

    """CONTROLE TOURNOI"""
    #Début du tounoi
    def startTournoi(self):
        return self.tournoi.startTournoi()
    
    #Si le tournoi a débuté
    def isStarted(self):
        return self.tournoi.started
    
    #Début de la ronde
    def startRonde(self):
        return self.tournoi.newRound()
    
    #Si la ronde a débuté
    def isStartedRonde(self):
        return self.tournoi.startedRonde
    
    def getRonde(self, rondeNumber):
        return self.tournoi.getRonde(rondeNumber)
            
    #Définir vainqueur
    def winner(self, tableNumber, pseudo):
        return self.tournoi.winner(tableNumber, pseudo)
    
    #Fin de la ronde
    def endRonde(self):
        return self.tournoi.calculPoints()
    
    def goBackRonde(self):
        self.tournoi.goBackRonde()

    #Si les tables ont fini de jouer
    def isAllFinishedTable(self):
        return self.tournoi.allFinishedTable()
    
    #Drop de joueur
    def dropPlayer(self, participant):
        self.tournoi.dropPlayer(participant)
    
    #Reset du tournoi
    def resetTournoi(self):
        self.tournoi.resetTournoi(True)
    """FIN CONTROLE TOURNOI"""