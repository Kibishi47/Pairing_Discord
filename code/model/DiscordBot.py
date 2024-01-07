import discord
from discord.ext import commands
from metier.Participant import Participant
from metier.Tounoi import Tournoi
#import disnake
#from disnake.ext import commands, tasks
#import os, random

class DiscordBot:
    def __init__(self, controller):
        self.controller = controller
        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix = "!", description = "Bot pairing DBS", intents=intents)
        self.token1 = "MTA5MTA2MTM3NDQ2NzE4NjczOA."
        self.token2 = "G6xpEi.CY7tET_YIflWXkFkc37CJQmcsaaBPthpfZpyQ8"
        #Channels autorisé
        self.CHANNELS = {
            "commande-bot": 1092116723722891354,
            "pairing": 1019536748969214013,
            "résultat": 1019536789901410325,
            "admin": 1138469514707750912,
        }
        self.FORUMS = {
            "test-command-forum": 1100036071913443448
        }

        #Quand le bot est ONLINE
        @bot.event
        async def on_ready():
            print("Ready !")
        
        #Fonction de vérification de channel
        def check_channel(ctx):
            if ctx.channel.type == discord.ChannelType.forum:
                if ctx.channel.parent.id not in self.FORUMS.values():
                    print(f"Channel incorrect")
                    return False
            else :
                if ctx.channel.type == discord.ChannelType.text:
                    if ctx.channel.id not in self.CHANNELS.values():
                        print(f"Channel incorrect")
                        return False
            return True


        """BASIC COMMAND"""
        #Efface les messages
        @bot.command()
        async def clr(ctx, nombre: int = 1, droit = False):
            if not ctx.author.guild_permissions.manage_messages and not droit :
                print(f"{ctx.author} n'est pas permis de supprimer des messages")
                return
            messages = []
            async for message in ctx.channel.history(limit=nombre + 1):
                messages.append(message)
            for message in messages:
                await message.delete()

        #Liste aux utilisateurs les commandes disponibles
        @bot.command()
        @commands.check(check_channel)
        async def command(ctx):
            await clr(ctx, 0, True)
            description = "() : Optionnel // [] : Obligatoire\n"
            description += "\n**Gestion de Participants**"
            description += "\n**add [pseudo:X]**: Ajout d'un participant"
            description += "\n**seePlayer (pseudo)**: Affiche un ou tous les participants"
            description += "\n**deletePlayer (pseudo)**: Supprime un ou tous les participants"
            description += "\n**modifyPlayer [pseudo] [pseudo:X]**: Modifier les données d'un participant"
            description += "\n"
            description += "\n**Gestion du Tournoi**"
            description += "\n**name [nom du tournoi]**: Nomme le tournoi"
            description += "\n**startTournoi**: Débute le tournoi"
            description += "\n**startRonde**: Débute une nouvelle ronde"
            description += "\n**pairing (numéro)**: Affiche le pairing d'une ronde"
            description += "\n**table [numéro] [pseudo vainqueur/draw]**: Défini le vainqueur à une table ou une égalité"
            description += "\n**endRonde**: Termine la ronde en cours"
            description += "\n**classement**: Affiche le classement actuel"
            
            embed = discord.Embed(
                title = "Voici les commandes disponibles", 
                description = description,
                color=discord.Color(0xC7819E)
            )
            
            await ctx.send(embed=embed)
        
        """FIN BASIC COMMAND"""


        """PARTICIPANT COMMAND"""
        #Ajout de participants
        @bot.command()
        @commands.check(check_channel)
        async def add(ctx, *, arg=""):
            if len(arg) == 0:
                await ctx.send("Veuillez donner les informations du participant")
                return
            
            #Toutes les informations sont correctes
            participant = Participant()
            participant.pseudo = arg.strip()
            if self.controller.searchParticipant(participant.pseudo) != None:
                await ctx.send("Ce participant existe déjà")
                return
            number_participants = self.controller.newParticipant(participant)
            str_number_participants = ""
            if number_participants > 1:
                str_number_participants = f"({number_participants} participants au tournoi)"
            await ctx.send(f"Participant ajouté ! {str_number_participants}")
            await self.printParticipant(ctx, [participant])
            
        #Voir les participants d'un tournoi
        @bot.command()
        @commands.check(check_channel)
        async def seePlayer(ctx, *, pseudo=""):
            await clr(ctx, 0, True)
            if len(pseudo) == 0:
                participants = self.controller.getParticipants()
                if len(participants) == 0:
                    await ctx.send("Il n'y a aucun joueur à ce tournoi !")
                else:
                    await self.printParticipant(ctx, participants)
                    #await ctx.send('\n'.join(str(participant) for participant in participants))
            else:
                pseudo = pseudo.strip()
                participant = self.controller.searchParticipant(pseudo)
                if participant == None:
                    await ctx.send(f"Aucun joueur ne possède le pseudo '{pseudo}'")
                else:
                    #await ctx.send(str(participant))
                    await self.printParticipant(ctx, [participant])
            
        #Clear les participants
        @bot.command()
        @commands.check(check_channel)
        async def deletePlayer(ctx, *, arg=""):
            if not ctx.author.guild_permissions.manage_messages:
                print(f"{ctx.author} n'est pas permis de supprimer un ou plusieurs participants")
                return
            if arg == "":
                pseudo = None
                await ctx.send("Tous les participants ont été supprimés")
            else:
                pseudo = arg
                participant = self.controller.searchParticipant(pseudo)
                if participant == None:
                    await ctx.send(f"Aucun joueur ne possède le pseudo '{pseudo}'")
                    return
                await ctx.send(f"{pseudo} a été supprimé")
            self.controller.clearParticipants(pseudo)
            
        #Modifier les informations d'un participant
        @bot.command()
        @commands.check(check_channel)
        async def modifyPlayer(ctx, pseudo="", *, arg=""):
            if len(pseudo) == 0:
                await ctx.send("Veuillez donner le pseudo du participant")
                return
            participant = self.controller.searchParticipant(pseudo)
            if participant is None:
                await ctx.send(f"Le participant '{pseudo}' n'existe pas.")
                return

            # Vérifier les informations à modifier
            if len(arg) == 0:
                await ctx.send("Veuillez fournir les nouvelles informations du participant.")
                return

            participant.pseudo = arg.strip()

            await ctx.send(f"Informations du participant '{pseudo}' modifiées.")
            #await ctx.send(str(participant))
            await self.printParticipant(ctx, [participant])
        
        #Participant par défaut
        @bot.command()
        @commands.check(check_channel)
        async def defaultPlayers(ctx):
            await clr(ctx, 0, True)
            players = [
                # {"pseudo": "beryu"},
                # {"pseudo": "nainain"},
                # {"pseudo": "sombros"},
                # {"pseudo": "kibishi"},
                {"pseudo": "sfnicolas"},
                {"pseudo": "Sylvain"},
                {"pseudo": "jsaispaski"},
                {"pseudo": "Argosax"},
                {"pseudo": "Nainaintcg"},
                {"pseudo": "Bull8"},
                {"pseudo": "beryu"},
                {"pseudo": "malhi"},
                {"pseudo": "Menmasan"},
                {"pseudo": "Alexxx"},
                {"pseudo": "Groot"},
                {"pseudo": "rydden"},
                {"pseudo": "Rishin"},
                {"pseudo": "Jordan"},
                {"pseudo": "Jefdu59"},
                {"pseudo": "william"},
                {"pseudo": "Kiva"},
                {"pseudo": "Gael"},
                {"pseudo": "Alister"},
                {"pseudo": "Sombros"},
                {"pseudo": "majindelena"},
                {"pseudo": "Lightside74"},
                {"pseudo": "Willy"},
            ]
            for player in players:
                participant = Participant()
                participant.pseudo = player["pseudo"]
                self.controller.newParticipant(participant)
            await ctx.send("20 joueurs par défaut insérés : ")
            await self.printParticipant(ctx, self.controller.getParticipants())
        
        """FIN PARTICIPANT COMMAND"""

        """GESTION TOURNOI"""
        #Set name
        @bot.command()
        @commands.check(check_channel)
        async def name(ctx, *, arg):
            await clr(ctx, 0, True)
            if not ctx.author.guild_permissions.manage_messages:
                print(f"{ctx.author} n'est pas permis d'attribuer un nom au tournoi")
                return
            self.controller.tournoi.name = arg
            await ctx.send(f"Le nom du tournoi est : {arg}")
        
        #AJOUT D'UN PING
        
        #Defaut
        @bot.command()
        @commands.check(check_channel)
        async def default(ctx):
            await clr(ctx, 0, True)
            await defaultPlayers(ctx)
            await ctx.send("msg temp")
            await startTournoi(ctx)
            await ctx.send("msg temp")
            await startRonde(ctx)
        
        #Début du tournoi
        @bot.command()
        @commands.check(check_channel)
        async def startTournoi(ctx):
            await clr(ctx, 0, True)
            if not ctx.author.guild_permissions.manage_messages:
                print(f"{ctx.author} n'est pas permis d'attribuer un nom au tournoi")
                return
            if self.controller.isStarted():
                await ctx.send("Le tournoi a déjà commencé !")
                return
            nbRound, top = self.controller.startTournoi()
            if nbRound != None and nbRound != 0:
                await ctx.send(f"Le tournoi commence !\n- Nombre de round : {nbRound}\n- Top : {'Aucun' if top == None else top}")
                return
            await ctx.send("Le tournoi ne peut pas commencer.\nIl y a une erreur")

        #Début de la ronde
        @bot.command()
        @commands.check(check_channel)
        async def startRonde(ctx):
            await clr(ctx, 0, True)
            if not ctx.author.guild_permissions.manage_messages:
                print(f"{ctx.author} n'est pas permis de démarrer une ronde")
                return
            if not self.controller.isStarted():
                await ctx.send("Le tournoi n'a pas encore commencé !")
                return
            if self.controller.isStartedRonde():
                await ctx.send("La ronde a déjà commencé !")
                return
            ronde = self.controller.startRonde()
            await self.printPairing(ctx, ronde)

        #Affichage du pairing d'une certaine Ronde
        @bot.command()
        @commands.check(check_channel)
        async def pairing(ctx, number=0):
            await clr(ctx, 0, True)
            ronde = self.controller.getRonde(number)
            if ronde == None:
                await ctx.send("Cette ronde n'existe pas")
                return
            await self.printPairing(ctx, ronde)

        #Définir le vainqueur
        @bot.command()
        @commands.check(check_channel)
        async def table(ctx, number=0, *, pseudo=""):
            if len(pseudo) == 0:
                await ctx.send("Veuillez donner les informations du match")
                return
            
            #Toutes les informations sont correctes
            info = self.controller.winner(number, pseudo)
            if info == "no-table":
                await ctx.send("Cette table n'existe pas !")
            elif info == "no-player":
                await ctx.send("Ce joueur n'est pas sur cette table !")
            elif info == "set-draw":
                await ctx.send(f"Il y a eu égalité à la table {number}")
            elif info == "set-winner":
                await ctx.send(f"{pseudo} est le vainqueur de la table {number} !")
            elif info == "no-change":
                await ctx.send(f"{pseudo} est déjà le vainqueur de la table {number} !")
            elif info == "change":
                await ctx.send(f"Modification du vainqueur\n{pseudo} est le vainqueur de la table {number} !")

        #Fin de round
        @bot.command()
        @commands.check(check_channel)
        async def endRonde(ctx):
            await clr(ctx, 0, True)
            if not ctx.author.guild_permissions.manage_messages:
                print(f"{ctx.author} n'est pas permis d'attribuer un nom au tournoi")
                return
            if not self.controller.isAllFinishedTable():
                await ctx.send("Les tables n'ont pas fini de jouer !")
                return
            if not self.controller.isStartedRonde:
                await ctx.send("Aucune ronde en cours !")
            info = self.controller.endRonde()
            if type(info) == str:
                await ctx.send(f"Le tournoi est terminé !\nLe vainqueur est {info} !!\nFÉLICITATION !!")
                await self.printClassement(ctx, self.controller.getSortedParticipants())
            else: 
                await ctx.send(f"Il reste encore {info} ronde{'s' if info>1 else ''} !")
        
        @bot.command()
        @commands.check(check_channel)
        async def returnRonde(ctx):
            await clr(ctx, 0, True)
            if not ctx.author.guild_permissions.manage_messages:
                print(f"{ctx.author} n'est pas permis de modifier la ronde en cours")
                return
            self.controller.goBackRonde()
            await ctx.send("Retour à la ronde précédente")


        #Affichage du classement
        @bot.command()
        @commands.check(check_channel)
        async def classement(ctx, arg = None):
            await clr(ctx, 0, True)
            if arg == None:
                await self.printClassement(ctx, self.controller.getSortedParticipants())
            elif arg == "admin":
                await self.printClassementAdmin(ctx, self.controller.getSortedParticipants())


        #Définir un drop de joueur
        @bot.command()
        @commands.check(check_channel)
        async def drop(ctx, pseudo = ""):
            if self.controller.isStartedRonde():
                await ctx.send("La ronde est toujours en cours !")
                return
            if len(pseudo) == 0:
                await ctx.send("Veuillez renseigner un joueur !")
                return
            pseudo = pseudo.strip()
            participant = self.controller.searchParticipant(pseudo)
            if participant == None:
                await ctx.send(f"Aucun joueur ne possède le pseudo '{pseudo}'")
            else:
                self.controller.dropPlayer(participant)
                await ctx.send(f"{pseudo} a drop ce tournoi !")
        
        #Fin du tournoi
        @bot.command()
        @commands.check(check_channel)
        async def endTournoi(ctx):
            await clr(ctx, 0, True)
            if not ctx.author.guild_permissions.manage_messages:
                print(f"{ctx.author} n'est pas permis de terminer le tournoi")
                return
            self.controller.resetTournoi()
            await ctx.send("Le tournoi prend fin !")
        
        """FIN GESTION TOURNOI"""


        bot.run(self.token1 + self.token2)


    #Fonction d'affichage de Participant
    async def printParticipant(self, ctx, participants):
        embed = discord.Embed(
            title="Participant" if len(participants) == 1 else f"Participants ({len(participants)})",
            color=0xC7819E
        )
        listPseudo = []
        
        for participant in participants:
            listPseudo.append(participant.pseudo)
            
        embed.add_field(name="Pseudo", value='\n'.join(listPseudo), inline=True)
        
        embed.set_author(name = self.controller.tournoi.name)
        
        await ctx.send(embed=embed)

    #Fonction d'affichage de Pairing
    async def printPairing(self, ctx, ronde):
        tables = ronde.tables
        embed = discord.Embed(
            title=f"Ronde {ronde.number}",
            color=0xC7819E
        )
        listJ1 = []
        listJ2 = []
        listTable = []

        for table in tables:
            J1 = table.participants[0].pseudo
            J2 = table.participants[1].pseudo
            if table.win == 0 or table.win == 1:
                if table.win == 0:
                    J2 = "~~" + J2 + "~~"
                else:
                    J1 = "~~" + J1 + "~~"

            listJ1.append(J1)
            listJ2.append(J2)
            listTable.append(str(table.number))
        
        embed.add_field(name="Joueur 1", value='\n'.join(listJ1), inline=True)
        embed.add_field(name="Joueur 2", value='\n'.join(listJ2), inline=True)
        embed.add_field(name="Table", value='\n'.join(listTable), inline=True)
        
        embed.set_author(name = self.controller.tournoi.name)

        await ctx.send(embed=embed)

    #Fonction d'affichage du classement
    async def printClassement(self, ctx, participants):
        embed = discord.Embed(
            title = "Classement",
            color = 0xC7819E
        )
        listRank = []
        listJoueur = []
        listPoints = []
        listTieBreaker = []

        for i in range(0, len(participants), 1):
            participant = participants[i]
            listRank.append(str(i+1))
            listJoueur.append(participant.pseudo)
            listPoints.append(str(participant.points))
            listTieBreaker.append(str(participant.tieBreaker))

        embed.add_field(name="Rank", value='\n'.join(listRank), inline=True)
        embed.add_field(name="Joueur", value='\n'.join(listJoueur), inline=True)
        embed.add_field(name="Points", value='\n'.join(listPoints), inline=True)
        #embed.add_field(name="TieBreaker", value='\n'.join(listTieBreaker), inline=True)

        embed.set_author(name = self.controller.tournoi.name)
        await ctx.send(embed=embed)

    #Fonction d'affichage du classement
    async def printClassementAdmin(self, ctx, participants):
        embed = discord.Embed(
            title = "Classement",
            color = 0xC7819E
        )
        listJoueur = []
        listPoints = []
        listTieBreaker = []

        for i in range(0, len(participants), 1):
            participant = participants[i]
            listJoueur.append(participant.pseudo)
            listPoints.append(str(participant.points))
            listTieBreaker.append(str(participant.tieBreaker))

        embed.add_field(name="Joueur", value='\n'.join(listJoueur), inline=True)
        embed.add_field(name="Points", value='\n'.join(listPoints), inline=True)
        embed.add_field(name="TieBreaker", value='\n'.join(listTieBreaker), inline=True)

        embed.set_author(name = self.controller.tournoi.name)
        await ctx.send(embed=embed)