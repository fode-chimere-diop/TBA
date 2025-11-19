# Classe représentant le joueur
class Player():

    def __init__(self, nom):
        # Nom du joueur
        self.nom = nom
        # La pièce où se trouve actuellement le joueur (sera définie plus tard)
        self.piece = None
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
        if self.piece is None:
            print("\nErreur : le joueur n'est dans aucune salle.\n")
            return False

        # Vérifie si la direction existe dans les exits
        if direction not in self.piece.exits:
            print("\nDirection inconnue ! (N/S/E/O)\n")
            return False

        prochaine_piece = self.piece.exits[direction]

        if prochaine_piece is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        # Déplacement effectif
        self.piece = prochaine_piece
        print(self.piece.get_long_description())
        return True
