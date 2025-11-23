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

        # Déplacement effectif
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True
