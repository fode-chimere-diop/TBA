"""Define the Player class."""

from quest import QuestManager
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
        self.move_count = 0
        self.quest_manager = QuestManager(self)
        self.rewards = []  # List to store earned rewards
      # Define the move method.

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
            print("\nDirection inconnue ! (N/S/E/O/U)\n")
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
        if self.current_room.name == "salle_secréte":
            # On supprime la sortie Sud pour bloquer le retour
            if "S" in self.current_room.exits:
                self.current_room.exits["S"] = None
            print("\n" + "!"*50)
            print("🚨 CLAC ! La trappe se verrouille derrière vous.")
            print("Vous êtes au sommet. Il n'y a plus aucun moyen de redescendre.")
            print("Le trésor est à portée de main... si vous avez le code.")
            print("!"*50 + "\n")
            self.quest_manager.activate_quest("Le Secret du Sommet")

        # 🎯 Activation des quêtes de niveau 2 quand on arrive dans hall_1
        if self.current_room.name == "hall_1":
            qm = self.quest_manager

            qm.activate_quest("Énigme de Mr_Red")
            qm.activate_quest("Énigme de Mr_White")
            qm.activate_quest("Énigme de Mr_Blue")
        # Dans player.py, méthode move
        if self.current_room.name == "terrasse_2" or self.current_room.name == "restaurant":
            self.quest_manager.activate_quest("Le Protocole du Sommet")
        

          # Check room visit objectives
        self.quest_manager.check_room_objectives(self.current_room.name)

        # Increment move counter and check movement objectives
        self.move_count += 1
        self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)

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
    # Dans player.py
    def get_inventory(self):
        if not self.inventaire:
            return "Votre inventaire est vide."
    
        texte = "Vous possédez :\n"
        for item in self.inventaire:
        # ✅ AJOUTE .nom ICI pour que ce soit clair
            texte += f"    - {item.nom} : {item.description}\n" 
        return texte
    #pour voir
    def check(self):
        """
        Affiche le contenu de l'inventaire du joueur de façon claire.
        """
        if len(self.inventaire) == 0:
            return "Votre inventaire est vide.\n"

        txt = "Vous possédez :\n"
        for item in self.inventaire:
            # ✅ On affiche le NOM et la DESCRIPTION pour que ce soit clair
            txt += f" - {item.nom} : {item.description} ({item.poids} kg)\n"
        return txt
#pour la limite du poids
    def current_weight(self):
        """
    Calcule le poids total de l'inventaire
        """
        total = 0
        for item in self.inventaire:
            total += item.poids
        return total
    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.
        
        Args:
            reward (str): The reward to add.
            
        Examples:
        
        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            #print(f"\n🎁 Vous avez obtenu: {reward}\n")


    def show_rewards(self):
        """
        Display all rewards earned by the player.
        
        Examples:
        
        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()