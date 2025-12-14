# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1].lower() 
        if direction in ("n", "nord"): # condition pour go Nord ou go N 
            direction = "N"
        elif direction in ("s", "sud"):
            direction = "S"
        elif direction in ("e", "est"):
            direction = "E"
        elif direction in ("o", "ouest"):
            direction = "O"
        else:
            print(f"\nDirection '{list_of_words[1]}' non reconnue.\n")
            return False
        # Move the player in the direction specified by the parameter. 
        player.move(direction)

        return True

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.nom} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
      # 🔹 Nouvelle action : afficher l'historique sur commande
    def history(game, list_of_words, number_of_parameters): #ajouter pour l'historique
        """
        Affiche l'historique des pièces déjà visitées.
        """
        l = len(list_of_words)
        # Pas de paramètre attendu
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        print(game.player.get_history())
        return True
    def back(game, list_of_words, number_of_parameters): #ajouter pour le back 
        """
    Revenir à la pièce précédente.
    Impossible si aucune pièce n'a encore été visitée.
        """
        player = game.player
        l = len(list_of_words)

        # La commande back ne prend aucun paramètre
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Vérifier si retour possible
        if len(player.history) == 0:
            print("\nVous ne pouvez plus reculer davantage : impossible de revenir en arrière.\n")
            return False

        # Retirer la dernière salle visitée
        previous_room = player.history.pop()

        # Mise à jour de la salle courante
        player.current_room = previous_room

        # Affichage de la nouvelle salle
        print(player.current_room.get_long_description())

        # Affichage de l'historique mis à jour
        print(player.get_history())

        return True
    # pour le look

    def look(game, list_of_words, number_of_parameters):
        """
    Affiche la description de la pièce où se trouve le joueur
    ainsi que les objets présents dans cette pièce.
        """

    # Vérifier qu'il n'y a pas de paramètre supplémentaire
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(f"Commande incorrecte : {command_word}")
            return False

        room = game.player.current_room
        if room is None:
            print("\nVous n'êtes dans aucune pièce.\n")
            return False

    #description de la pièce
        print(room.get_long_description())

    #affichage des items
        print(room.get_inventory())

        return True
#pour pouvoir prendre l'objet
    def take(game, list_of_words, number_of_parameters):
        """
    Permet de prendre un objet dans la pièce et de le mettre dans l'inventaire du joueur.
    Syntaxe : take <nom_item>
        """

    # Vérifie le nombre de paramètres
        if len(list_of_words) != number_of_parameters + 1:
            print("Commande incorrecte : utilisez 'take <nom_item>'")
            return False

        item_name = list_of_words[1].lower()
        player = game.player
        room = player.current_room

        if not room.inventaire:
            print("Il n'y a aucun objet à prendre ici.")
            return False

    # Cherche l'objet dans l'inventaire de la pièce
        for item in room.inventaire:
            if item.nom.lower() == item_name:

            #VÉRIFICATION DU POIDS
                poids_actuel = player.current_weight()
                if poids_actuel + item.poids > player.max_weight:
                    print(
                        f"Impossible de prendre {item.nom} : "
                        f"poids maximal dépassé "
                        f"({poids_actuel}/{player.max_weight})"
                    )
                    return False

            # Ajoute à l'inventaire du joueur
                player.inventaire.append(item)

            # Retire de la pièce
                room.inventaire.remove(item)

            # Mets à jour l'état du joueur si besoin
                if item.nom.lower() == "eclair":
                    player.eclair_choco = True
                elif item.nom.lower() == "tournevis":
                    player.tournevis = True

                print(f"Vous avez pris : {item.nom}")
                return True

    # Si l'objet n'a pas été trouvé
        print(f"L'objet '{item_name}' n'est pas dans cette pièce.")
        return False

    #pour l'inventaire
    def inventory(game, list_of_words, number_of_parameters):
        """
    Affiche l'inventaire du joueur.
    Syntaxe : inventory
        """
        if len(list_of_words) != number_of_parameters + 1:
            print("Commande incorrecte : utilisez 'inventory'")
            return False

        if not game.player.inventaire:
            print("Votre inventaire est vide.")
            return True

        print("Vous possédez :")
        for item in game.player.inventaire:
            print(f" - {item.nom} : {item.description} ({item.poids} kg)")
        return True
    def drop(game, list_of_words, number_of_parameters):
        """
    Repose un item de l'inventaire du joueur dans la pièce actuelle.
    Syntaxe : drop <nom_item>
        """
    # Vérification du nombre de paramètres
        if len(list_of_words) != number_of_parameters + 1:
            print("Utilisation : drop <item>")
            return False

        player = game.player
        room = player.current_room
        item_name = list_of_words[1].lower()

    # Cherche l'item dans l'inventaire du joueur
        item_to_drop = None
        for item in player.inventaire:
            if item.nom.lower() == item_name:
                item_to_drop = item
                break

        # Si l'item n'est pas dans l'inventaire
        if item_to_drop is None:
            print(f"Vous n'avez pas '{item_name}' dans votre inventaire.")
            return False

        # Déposer l'item
        player.inventaire.remove(item_to_drop)
        room.inventaire.append(item_to_drop)

        print(f"Vous avez reposé {item_to_drop.nom}.")
        return True
    def check(game, list_of_words, number_of_parameters):
        """
    Affiche l'inventaire du joueur
        """

    # check ne prend aucun paramètre
        if len(list_of_words) != number_of_parameters + 1:
            print("Utilisation : check")
            return False

        player = game.player
        print(player.check())
        return True



