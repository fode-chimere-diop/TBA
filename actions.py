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
    @staticmethod
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
    @staticmethod
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
    @staticmethod
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
            # 🔒 Bloquer l'éclair si la machine n'est pas réparée
            if item.nom.lower() == "eclair" and not game.machine_reparee:
                print("La machine est cassée. Impossible de prendre l'éclair.")
                return False
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
    #interagir avec les pnj
    @staticmethod
    def talk(game, list_of_words, number_of_parameters):
        """
        talk <someone> : fait parler un PNJ présent dans la pièce.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        room = player.current_room
        target = list_of_words[1].strip().lower()

        for name, character in room.characters.items():
            if name.lower() == target:
                # On valide l'objectif "parler" dans le QuestManager (si besoin)
                game.player.quest_manager.check_action_objectives("parler", character.name)

                # Dialogue du GARDE (Indice seulement)
                if character.name.lower() == "garde":
                    print("\nGarde : 'Halte ! Je ne laisse passer personne sans une autorisation... ou un bon éclair au chocolat.'")
                    return True

                # Dialogue du BOULANGER (Indice seulement)
                elif character.name.lower() == "boulanger":
                    if game.machine_reparee:
                        print("\nBoulanger : 'Merci encore pour votre aide ! Mes éclairs sont à votre disposition.'")
                    else:
                        print("\nBoulanger : 'Quelle catastrophe... Ma machine est en panne. Il me faudrait un tournevis pour la réparer.'")
                    return True
                # Dialogue des autres PNJ avec énigmes (niveau 2)
                #dialogue Mr_red
                if character.name.lower() == "mr_red":
                    game.mr_red_enigme_donnee = True
                    character.get_msg()
                    return True
                #dialogue  Mr White
                if character.name.lower() == "mr_white":
                    game.mr_white_enigme_donnee = True
                    character.get_msg()
                    return True
                #dialogue Mr blue
                if character.name.lower() == "mr_blue":
                    game.mr_blue_enigme_donnee = True
                    character.get_msg()
                    return True

                # Autres PNJ (messages en boucle)
                character.get_msg()
                return True 

        print(f"\nIl n'y a pas de '{list_of_words[1]}' ici.\n")
        return False

    # --- MÉTHODE GIVE (Action réelle) ---
    @staticmethod
    def give(game, list_of_words, number_of_parameters):
        """
        Syntaxe : give <objet> <personnage>
        """
        if len(list_of_words) != 3:
            print("Utilisation : give <objet> <personnage>")
            return False

        item_name = list_of_words[1].lower()
        target = list_of_words[2].lower()
        player = game.player
        room = player.current_room

        # 1. Vérifier que le PNJ est bien présent
        if target not in [n.lower() for n in room.characters.keys()]:
            print(f"{target} n'est pas ici.")
            return False

        # 2. Chercher l'objet dans l'inventaire du joueur
        item_to_give = None
        for item in player.inventaire:
            if item.nom.lower() == item_name:
                item_to_give = item
                break

        if item_to_give is None:
            print(f"Vous n'avez pas de '{item_name}' dans votre inventaire.")
            return False

        # --- LOGIQUE DES ÉCHANGES ---

        # CAS DU GARDE (L'Éclair)
        if target == "garde" and item_name == "eclair":
            print(f"\nVous donnez l'éclair au garde.")
            print("Garde : 'Oh merci ! Il a l'air délicieux. Allez, je vous laisse passer !'")
            print("Le garde vous glisse un secret : 'Retenez bien ce chiffre pour le code final : 8'")
            
            player.inventaire.remove(item_to_give)
            game.eclair_donne_au_garde = True # Déclenche la victoire (win)
            player.quest_manager.check_action_objectives("donner", "eclair")
            return True

        # CAS DU BOULANGER (Le Tournevis)
        if target == "boulanger" and item_name == "tournevis":
            print(f"\nVous donnez le tournevis au boulanger.")
            print("Boulanger : 'Merci ! Je répare la machine tout de suite. Voilà, elle fonctionne !'")
            
            player.inventaire.remove(item_to_give)
            game.machine_reparee = True # Débloque la prise de l'éclair (take)
            player.quest_manager.check_action_objectives("donner", "tournevis")
            return True
        #  MR_RED — Énigme du drapeau
        if target == "mr_red":
            if item_name in ("drapeau_sénégal", "drapeau_senegal"):
                print("\nMr_Red : 'Correct.'")

                player.inventaire.remove(item_to_give)
                game.mr_red_enigme_resolue = True

                player.quest_manager.check_action_objectives("donner", "drapeau_sénégal")
                game.try_spawn_france_pnj()
                return True
            else:
                print("Mr_Red : 'Non. Ce n'est pas le bon drapeau.'")
                return False
        # ⚪ MR_WHITE — Énigme Turquie
        if target == "mr_white":
            if item_name == "drapeau_turquie":
                print("\nMr_White : 'Exact. Tu as l'esprit vif.'")
        
                player.inventaire.remove(item_to_give)
                game.mr_white_enigme_resolue = True

                player.quest_manager.check_action_objectives("donner", "drapeau_Turquie")
                game.try_spawn_france_pnj()
                return True
            else:
                print("Mr_White : 'Faux. Ce n'est pas le bon drapeau.'")
                return False
        # 🔵 MR_BLUE — Énigme Mexique
        if target == "mr_blue":
            if item_name == "drapeau_mexique":
                print("\nMr_Blue : 'Exact. Tu as bien observé.'")
                print("Mr_Blue : 'Voici ton indice : chiffre 1.'")

                player.inventaire.remove(item_to_give)
                game.mr_blue_enigme_resolue = True

                player.quest_manager.check_action_objectives("donner", "drapeau_Mexique")
                game.try_spawn_france_pnj()
                return True
            else:
                print("Mr_Blue : 'Non. Ce n'est pas le bon drapeau.'")
                return False

        print(f"{target} ne veut pas de cet objet.")
        return False
    
    #GIVE
    #@staticmethod
    """def give(game, list_of_words, number_of_parameters):
        Syntaxe : give <objet> <personnage>
        if len(list_of_words) != 3:
            print("Utilisation : give <objet> <personnage>")
            return False

        item_name = list_of_words[1].lower()
        target = list_of_words[2].lower()
        player = game.player
        room = player.current_room

        # 1. Vérifier que le PNJ est bien présent dans la pièce
        if target not in [n.lower() for n in room.characters.keys()]:
            print(f"{target} n'est pas ici.")
            return False

        # 2. Chercher l'objet dans l'inventaire du joueur
        item_to_give = None
        for item in player.inventaire:
            if item.nom.lower() == item_name:
                item_to_give = item
                break

        if item_to_give is None:
            print(f"Vous n'avez pas de '{item_name}' dans votre inventaire.")
            return False

        # --- LOGIQUE SPÉCIFIQUE POUR LES ÉCHANGES ---

        # CAS DU GARDE (L'Éclair)
        if target == "garde" and item_name == "eclair":
            print(f"\nVous donnez l'éclair au garde.")
            print("Garde : 'Oh merci ! Il a l'air délicieux. Vous pouvez passer !'")
            
            player.inventaire.remove(item_to_give)
            game.eclair_donne_au_garde = True # Déclenche la victoire
            
            # Validation de la quête
            player.quest_manager.check_action_objectives("donner", "eclair")
            return True

        # CAS DU BOULANGER (Le Tournevis)
        if target == "boulanger" and item_name == "tournevis":
            print(f"\nVous donnez le tournevis au boulanger.")
            print("Boulanger : 'Merci ! Je vais pouvoir réparer la machine à éclairs.'")
            
            player.inventaire.remove(item_to_give)
            game.machine_reparee = True # Débloque l'item éclair dans la pièce
            
            # Validation d'une éventuelle quête
            player.quest_manager.check_action_objectives("donner", "tournevis")
            return True

        # Si ce n'est pas le bon objet ou le bon PNJ
        print(f"{target} ne sait pas quoi faire de cet objet.")
        return False
    """
# ajout pour les quetes
    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True


    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True


    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False


    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True
    @staticmethod
    def colors(game, list_of_words, number_of_parameters):
        """
    Mini-jeu: proposer un ordre de 5 couleurs.
    Usage: colors R B J V O
    Retour: nombre de couleurs bien placées.
        """
    # Vérif nombre de paramètres (colors + 5)
        if len(list_of_words) != number_of_parameters + 1:
            print("\nUtilisation : colors R B J V O\n")
            return False
        room = game.player.current_room
        if room is None:
            print("\nVous n'êtes dans aucune pièce.\n")
            return False

    # (Optionnel) restreindre à la terrasse
        if room.name not in ("terrasse_1", "terrasse_2"):
            print("\nLe jeu des couleurs se fait sur la terrasse.\n")
            return False

    # Code attendu (doit exister dans Game.__init__)
        code = [c.upper() for c in game.couleurs_code]   # ex: ["R","B","J","V","O"]

    # Proposition du joueur
        guess = [w.upper() for w in list_of_words[1:]]

        allowed = {"R", "B", "J", "V", "O"}

    # Vérif: lettres autorisées
        for c in guess:
            if c not in allowed:
                print(f"\nCouleur '{c}' invalide. Utilise seulement : R B J V O\n")
                return False

    # Vérif: 5 couleurs différentes (optionnel mais conseillé)
        if len(set(guess)) != 5:
            print("\nTu dois donner 5 couleurs différentes (pas de doublons).\n")
            return False

    # Comptage des bonnes réponses BIEN PLACÉES
        good = 0
        for i in range(5):
            if guess[i] == code[i]:
                good += 1

    # Résultat
        if good == 5:
            print("\n🎉 BRAVO ! Tu as trouvé le bon ordre !")
            print("Le PNJ te laisse passer vers le niveau 4.\n")
            game.acces_niveau_4 = True
            return True

        print(f"\n❌ Pas encore. Il y a {good} bonne(s) réponse(s) bien placée(s).\n")
        return True




