# Description: Game class

# Import modules
from room import Room
from player import Player
from item import Item
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.start_room = None  #  on crée une variable pour la pièce de départ
    
    # Setup the game
    def setup(self):

        # Setup commands
        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help

        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit

        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go

        history_cmd = Command("history", " : afficher l'historique des pièces visitées", Actions.history, 0)
        self.commands["history"] = history_cmd #ajouter pour l'historique

        back_cmd = Command("back", " : revenir à la pièce précédente", Actions.back, 0)
        self.commands["back"] = back_cmd #ajouter pour back
        
        # Setup rooms
        # Niveau 1
        hall_0 = Room("hall_0", "dans le hall du rez-de-chaussée")
        #je vais mettre le texte ici
        self.rooms.append(hall_0)
        boulangerie = Room("boulangerie", "dans la boulangerie")
        #trouver une solution pour eviter trop de \n
        self.rooms.append(boulangerie)
        salle_du_garde = Room("salle_du_garde", "")
        self.rooms.append(salle_du_garde)
        local_technique = Room("local_technique", "")
        self.rooms.append(local_technique)

        # Niveau 2
        escalier_vers_le_1er = Room("escalier_vers_le_1er", "")
        self.rooms.append(escalier_vers_le_1er)
        hall_1 = Room("hall_1", "")
        self.rooms.append(hall_1)
        pays_1 = Room("pays_1", "")
        self.rooms.append(pays_1)
        pays_2 = Room("pays_2", "")
        self.rooms.append(pays_2)
        pays_3 = Room("pays_3", "")
        self.rooms.append(pays_3)

        # Niveau 3
        escalier_vers_le_2eme = Room("escalier_vers_le_2eme", "")
        self.rooms.append(escalier_vers_le_2eme)
        terrasse_1 = Room("terrasse_1","")     
        self.rooms.append(terrasse_1)  

        # Niveau 4
        terrasse_2 = Room("terrasse_2","")
        self.rooms.append(terrasse_2)
        restaurant = Room("restaurant","")
        self.rooms.append(restaurant)
        bar = Room("bar","")
        self.rooms.append(bar)
        cuisine = Room("cuisine","")
        self.rooms.append(cuisine)

        # Niveau 5
        salle_secréte = Room("salle_secréte","")
        self.rooms.append(salle_secréte)

        # Create exits for rooms

        hall_0.exits = {"N" : None, "E" : salle_du_garde, "S" : None, "O" : boulangerie}
        boulangerie.exits = {"N" : None, "E" : hall_0, "S" : None, "O" : None}
        salle_du_garde.exits = {"N" : None, "E" : None, "S" : local_technique, "O" :hall_0}
        local_technique.exits = {"N" : salle_du_garde, "E" : None, "S" : None, "O" : None}

        escalier_vers_le_1er.exits = {"N" : hall_1, "E" : None, "S" : hall_0, "O" : None}
        hall_1.exits = {"N" : pays_3, "E" : pays_1, "S" : escalier_vers_le_1er, "O" : pays_2}
        pays_1.exits = {"N" :None ,"E" : None, "S" : None, "O" : hall_1}
        pays_2.exits = {"N" :None ,"E" : hall_1, "S" : None, "O" : None}
        pays_3.exits = {"N" :None ,"E" : None, "S" : hall_1, "O" : None}

        escalier_vers_le_2eme.exits = {"N" :None ,"E" : terrasse_1, "S" : None, "O" : pays_3}
        terrasse_1.exits = {"N" :None ,"E" : None, "S" : None, "O" : escalier_vers_le_2eme}

        terrasse_2.exits = {"N" :None ,"E" : None, "S" : terrasse_1, "O" : restaurant}
        restaurant.exits = {"N" :cuisine ,"E" : terrasse_2, "S" : None, "O" : bar}
        bar.exits = {"N" :None ,"E" : restaurant, "S" : None, "O" : None}
        cuisine.exits = {"N" :None ,"E" : None, "S" : restaurant, "O" : None}
        salle_secréte.exits = {"N" :None ,"E" : None, "S" : cuisine, "O" : None}

        #ON DÉFINIT ICI la salle de départ du joueur
        self.start_room = hall_0



    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()

        # Loop until the game is finished
        while not self.finished:
            self.process_command(input("> "))

        return None


    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        if command_string.strip() == "":
           return

        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]

        if command_word not in self.commands.keys(): 
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n") 
        else: 
            command = self.commands[command_word] 
            command.action(self, list_of_words, command.number_of_parameters)


    # Print the welcome message
    def print_welcome(self):
        print("==========================================")
        print("        BIENVENUE A LA TOUR EIFFEL")
        print("==========================================")

        # ASCII ART (inchangé)
        effeil = r""" 
                                        
                                ⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣤⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⢞⣍⣂⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡷⠶⠋⠹⡞⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣃⡤⣶⠛⣷⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⠃⣏⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠋⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⡀⠀⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⣇⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⣿⠀⢹⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⣿⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢰⢻⠀⠸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⣸⢸⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠇⣿⠸⡄⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⡇⠀⡇⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⠀⡇⠀⣧⠀⢻⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢰⡇⠀⣿⠀⠘⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⣸⡀⠀⢽⣦⣀⣩⣉⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡿⢇⣿⣶⠶⠿⠟⠋⠉⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⠾⠛⠋⠉⣀⣠⣴⠖⠀⠰⣦⡀⠈⠳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡿⠐⢲⠉⠉⠀⣿⠀⠀⠀⢹⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀⡞⠀⠀⠀⣿⠀⠀⠀⠈⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇⠀⢰⡇⠀⠀⠀⢸⡄⠀⠀⠀⢸⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠁⢀⣾⠁⠀⠀⠀⠘⣿⠀⠀⠀⠈⢿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠇⠀⣼⡇⠀⠀⠀⠀⠀⣿⣦⠀⠀⠀⠘⠿⠿⠿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡟⠀⣸⣿⠁⠀⠀⠀⠀⣀⣛⣹⣤⣤⣤⣶⠶⢦⣄⠈⠳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⢿⣁⣘⣭⣵⣴⡶⠶⠶⠿⠛⠛⠉⠉⠉⠀⠀⠀⠈⣍⠳⠶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⠟⠛⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣆⠀⠀⠀⠀⠀⢹⣷⣦⣌⠙⠲⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⢠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⢹⡀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⠛⠀⠀⢠⡿⠤⢤⡤⠄⠀⠀⠘⠛⠿⢯⣍⠀⠈⣷⡄⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠃⠀⢀⣴⠋⠀⣚⣡⠤⠔⠒⠚⠛⠒⠦⢤⣤⣀⡀⠸⣿⣆⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⢠⡞⠁⠀⣠⢟⣭⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣶⣄⡈⠧⠀⠀⠀⠀⠙⣿⣿⠀⠉⠙⢷⡄⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⢀⣴⠏⠀⠀⣀⡿⣫⣤⠶⠶⢶⣦⡀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠶⠚⠻⣿⣦⡀⠀⠀⠀⠀⠙⣿⣆⠀⠀⠀⢻⣆⡀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢀⡾⠃⠀⢀⣴⠏⠞⠉⠁⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⣠⠞⠉⠀⠀⠀⠀⠈⢻⣿⣆⠀⠀⠀⠀⠈⣿⣦⠀⠀⠀⠙⢷⡄⠀⠀⠀
        ⠀⠀⠀⣰⡿⠃⠀⢠⣾⠇⠀⠀⠀⠀⠀⠀⢀⣿⡇⠀⠀⠀⠀⣼⠟⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣧⠀⠀⠀⠀⠈⢿⣧⡀⠀⠀⠈⢿⣆⠀⠀
        ⠀⢀⣼⡟⠀⠀⢠⣿⠇⠀⠀⠀⠀⠀⠀⠀⢸⣿⣅⣀⡀⠀⢠⣿⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣧⠀⠀⠀⠀⠈⢻⣧⡄⠀⠀⠀⢻⣧⠀
        ⢠⣿⣏⡀⠀⠀⣾⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣦⠀⠀⠀⠀⢀⣿⣷⣄⠀⠒⠚⠛⠓
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠀⠀⠀⠒⠛⠉⠉⠛⠂⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠲⡆⠄⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀
        """
        print(effeil)
        
        # Création du joueur
        self.player = Player(input("\nQuel est ton nom ? : "))
        print(f"\nBienvenue {self.player.nom} !")
        print()
        print("Entrez 'help' si vous avez besoin d'aide.")
        print("==========================================")
        print("Tu te trouves maintenant au pied de la Tour Eiffel.")
        print("Un mystérieux trésor serait caché au sommet")
        print("de la Tour Eiffel... Mais seuls les plus")
        print("courageux peuvent atteindre le 4ème étage.")
        print("Ton objectif : monter jusqu'au 4ème étage ")
        print("et trouver le croissant d'or.")
        print("Chaque étage de la Tour Eiffel cache un défi unique.")
        print("Réussis les épreuves, collecte tous les chiffres")
        print("Et Va Decrocher le CROISSANT D’OR !")
        print("==========================================")
        input("\nAppuie sur [ENTRER] pour entrer dans le hall du rez-de-chaussée...")
        print()

        self.player.current_room = self.start_room

        print(self.player.current_room.get_long_description())



def main():
    Game().play()
    

if __name__ == "__main__":
    main()