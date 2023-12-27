finalParticipants = [
    "1", "2", "3"
]

participants = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"
]

# Calculer la longueur de la liste
longueur_liste = len(participants)

# Calculer la taille des groupes en privilégiant un groupe plus grand si la liste est impaire
taille_groupe1 = longueur_liste // 2 + (longueur_liste % 2)
taille_groupe2 = longueur_liste // 2

# Diviser la liste en deux groupes
groupe1 = participants[:taille_groupe1]
groupe2 = participants[taille_groupe1:taille_groupe1+taille_groupe2]

# Initialiser la liste finale
liste_finale = []

# Croiser les éléments des deux groupes
for i in range(max(len(groupe1), len(groupe2))):
    if i < len(groupe1):
        liste_finale.append(groupe1[i])
    if i < len(groupe2):
        liste_finale.append(groupe2[i])

# Afficher la liste finale
finalParticipants.extend(participants)
print("Liste finale croisée :", finalParticipants)