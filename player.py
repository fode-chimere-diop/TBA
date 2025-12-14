# Classe représentant le joueur bon
class Player():

    def __init__(self, nom):
        # Nom du joueur
        self.nom = nom
        # La pièce où se trouve actuellement le joueur (sera définie plus tard)
        self.current_room = None
        # Inventaire du joueur (objets collectés etc )
        self.inventaire = []            # exemple : ["tournevis", "éclair"]

        # Variables d'état pour suivre sa progression
        self.nombre = False            # pas de chiffre pour le moment
        self.nord = 0                  # compteur pour savoir s'il essaie d'aller au Nord alors que l'étage est verrouillé
        self.eclair_choco = False      # pas eclair pour le moment
        self.tournevis = False         # pas de tournevis pour le moment
        self.history = [] #ajouter pour historique 
        #ajouter pour limiter le nombre d'objet 
        self.max_weight = 10   # capacité maximale (ex: 10)

    # Déplace le joueur dans la direction demandée
    def move(self, direction):
        """
        direction : 'N', 'S', 'E', 'O' 
        Permet de déplacer le joueur d'une salle à une autre selon piece.exits
        """
        direction = direction.upper()

        # Vérifie si la pièce actuelle existe
        if self.current_room is None:
            print("\nErreur : le joueur n'est dans aucune salle.\n")
            return False

        # Vérifie si la direction existe dans les exits
        if direction not in self.current_room.exits:
            print("\nDirection inconnue ! (N/S/E/O)\n")
            return False

        next_room = self.current_room.exits[direction]

        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        # On utilise bien la méthode append() de la liste.
        self.history.append(self.current_room) #ajouter pour l'historique
        # Déplacement effectif
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True
    def get_history(self): #ajouter pour l'historique
        """
        Retourne une chaîne de caractères représentant les pièces déjà visitées
        (celles que le joueur a quittées).
        """
        if not self.history:
            return "\nVous n'avez pas encore visité d'autres pièces.\n"

        s = "\nVous avez déjà visité les pièces suivantes:\n"
        # On affiche les descriptions dans l'ordre de visite.
        for room in self.history:
            s += f" - {room.description}\n"
        return s
    def get_inventory(self):
        if not self.inventaire:
            return "Votre inventaire est vide."
    
        texte = "Vous possédez :\n"
        for item in self.inventaire:
            texte += f"    - {item}\n"
        return texte
    #pour voir
    def check(self):
        """
    Affiche le contenu de l'inventaire du joueur
        """
        if len(self.inventaire) == 0:
            return "Votre inventaire est vide.\n"

        txt = "Vous possédez :\n"
        for item in self.inventaire:
            txt += f" - {item}\n"
        return txt
#pour la limite du poids
    def current_weight(self):
        """
    Calcule le poids total de l'inventaire
        """
        total = 0
        for item in self.inventaire:
            total += item.weight
        return total
